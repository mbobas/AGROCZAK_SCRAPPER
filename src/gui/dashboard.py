"""
GUI Dashboard - Streamlit interface.
Uruchom: streamlit run src/gui/dashboard.py
"""
import sys
from pathlib import Path
from datetime import datetime
import json
import time
import threading
import warnings

warnings.filterwarnings('ignore')

# Dodaj sciezke
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd

from src.core.processor import ProductProcessor, ProcessorConfig, InputProduct, ProductResult
from src.core.cache import ProductCache
from src.api.allegro import AllegroClient, AllegroAPIError
from src.api.scraper import ScrapeDoClient, ScraperError


st.set_page_config(
    page_title="Allegro Price Monitor",
    page_icon="📊",
    layout="wide"
)


def init_session_state():
    """Inicjalizuje stan sesji."""
    if "processor" not in st.session_state:
        st.session_state.processor = None
    if "results" not in st.session_state:
        st.session_state.results = []
    if "running" not in st.session_state:
        st.session_state.running = False
    if "progress" not in st.session_state:
        st.session_state.progress = 0
    if "total" not in st.session_state:
        st.session_state.total = 0
    if "config" not in st.session_state:
        st.session_state.config = ProcessorConfig.from_yaml()
    if "scrape_client" not in st.session_state:
        st.session_state.scrape_client = None
    if "credits_info" not in st.session_state:
        st.session_state.credits_info = None


def get_scrape_client():
    """Pobiera lub tworzy klienta scrape.do."""
    if st.session_state.scrape_client is None:
        try:
            st.session_state.scrape_client = ScrapeDoClient()
        except ValueError:
            return None
    return st.session_state.scrape_client


def refresh_credits_info():
    """Odświeża informacje o kredytach (max 10/min)."""
    client = get_scrape_client()
    if client:
        info = client.get_credits_info()
        if "error" not in info:
            st.session_state.credits_info = info
            return info
    return None


def sidebar_config():
    """Panel konfiguracji w sidebarze."""
    st.sidebar.header("⚙️ Konfiguracja")
    
    config = st.session_state.config
    
    st.sidebar.subheader("Progi cenowe")
    min_markup = st.sidebar.slider(
        "Min. marża (%)", 0, 50, int(config.min_markup * 100)
    ) / 100
    max_markup = st.sidebar.slider(
        "Max. marża (%)", 0, 50, int(config.max_markup * 100)
    ) / 100
    
    st.sidebar.subheader("Sprzedaż")
    min_buyers = st.sidebar.number_input(
        "Min. kupujących", 0, 100, config.min_buyers
    )
    
    st.sidebar.subheader("Cache")
    ttl_days = st.sidebar.number_input(
        "Ważność danych (dni)", 1, 30, config.ttl_days
    )
    
    st.sidebar.subheader("Rate limiting")
    delay = st.sidebar.number_input(
        "Opóźnienie (s)", 1, 60, int(config.delay_seconds)
    )
    
    # Aktualizuj config
    st.session_state.config = ProcessorConfig(
        min_markup=min_markup,
        max_markup=max_markup,
        min_buyers=min_buyers,
        ttl_days=ttl_days,
        delay_seconds=float(delay)
    )
    
    # Źródło danych
    st.sidebar.subheader("Źródło danych")
    source = st.sidebar.selectbox(
        "Wybierz źródło",
        ["api", "scrape_do"],
        help="api = API Allegro (wymaga weryfikacji), scrape_do = scraping"
    )
    st.session_state.data_source = source
    
    # Cache stats
    st.sidebar.subheader("📦 Cache")
    cache = ProductCache()
    stats = cache.get_stats()
    st.sidebar.metric("Produktów w cache", stats["total_products"])
    
    if st.sidebar.button("🗑️ Wyczyść cache"):
        cache.clear_all()
        st.sidebar.success("Cache wyczyszczony!")
        st.rerun()
    
    # Kredyty scrape.do
    st.sidebar.divider()
    st.sidebar.subheader("💳 Kredyty scrape.do")
    
    client = get_scrape_client()
    if client:
        # Pokaż ostatnie znane dane lub odśwież
        if st.session_state.credits_info:
            info = st.session_state.credits_info
        else:
            info = refresh_credits_info()
        
        if info and "error" not in info:
            remaining = info.get('RemainingMonthlyRequest', 0)
            max_credits = info.get('MaxMonthlyRequest', 1000)
            used = max_credits - remaining
            usage_pct = (used / max_credits * 100) if max_credits > 0 else 0
            
            # Metryki
            col1, col2 = st.sidebar.columns(2)
            with col1:
                st.metric("Pozostało", f"{remaining:,}")
            with col2:
                st.metric("Użyto", f"{used:,}")
            
            # Pasek postępu zużycia
            st.sidebar.progress(min(usage_pct / 100, 1.0))
            st.sidebar.caption(f"Zużycie: {usage_pct:.1f}% ({used:,} / {max_credits:,})")
            
            # Limit równoczesnych
            concurrent = info.get('RemainingConcurrentRequest', 0)
            st.sidebar.caption(f"Równoczesne zapytania: {concurrent}")
            
            # Koszty
            st.sidebar.caption("""
            **Koszty:**
            - render=true: 5 kred./zapytanie
            - render=false: 1 kred./zapytanie
            """)
        else:
            st.sidebar.warning("Nie można pobrać info o kredytach")
        
        # Przycisk odświeżania (max 10/min)
        if st.sidebar.button("🔄 Odśwież kredyty"):
            new_info = refresh_credits_info()
            if new_info and "error" not in new_info:
                st.sidebar.success("Odświeżono!")
            else:
                st.sidebar.error(new_info.get("error", "Błąd") if new_info else "Błąd")
            st.rerun()
    else:
        st.sidebar.warning("Brak tokena scrape.do w .env")


def upload_section():
    """Sekcja uploadu pliku."""
    st.header("📁 Plik wejściowy")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Wybierz plik CSV (EAN;cena;nazwa)",
            type=["csv"],
            help="Plik CSV z kolumnami: ean, cena, nazwa (opcjonalnie)"
        )
    
    with col2:
        st.info("""
        **Format pliku:**
        ```
        ean;cena;nazwa
        5902719471797;100.00;Produkt 1
        ```
        """)
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file, sep=";")
            st.success(f"Wczytano {len(df)} produktów")
            st.dataframe(df.head(10), use_container_width=True)
            st.session_state.input_df = df
            return df
        except Exception as e:
            st.error(f"Błąd wczytywania: {e}")
    
    return None


def cost_estimate_section(num_products: int):
    """Sekcja szacowania kosztów."""
    client = get_scrape_client()
    if not client or num_products == 0:
        return True
    
    st.subheader("💰 Szacowany koszt")
    
    # Szacuj koszty
    estimate = client.estimate_cost(num_products, render=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Produktów", num_products)
    
    with col2:
        st.metric("Koszt (kredyty)", estimate['total_cost'])
    
    with col3:
        remaining = estimate['remaining_credits']
        if remaining is not None:
            st.metric("Pozostanie", remaining - estimate['total_cost'])
    
    # Sprawdź czy wystarczy kredytów
    if estimate['enough_credits'] is False:
        st.error(f"⚠️ Za mało kredytów! Potrzebujesz {estimate['total_cost']}, masz {remaining}")
        st.info(f"Możesz sprawdzić max {estimate['can_process']} produktów")
        return False
    elif estimate['enough_credits']:
        st.success(f"✅ Wystarczająco kredytów ({remaining} dostępnych)")
    
    return True


def control_section():
    """Sekcja kontroli procesu."""
    st.header("🎮 Kontrola")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        start_btn = st.button("▶️ Start", disabled=st.session_state.running)
    
    with col2:
        pause_btn = st.button("⏸️ Pauza", disabled=not st.session_state.running)
    
    with col3:
        resume_btn = st.button("▶️ Wznów", disabled=not st.session_state.running)
    
    with col4:
        stop_btn = st.button("⏹️ Stop", disabled=not st.session_state.running)
    
    return start_btn, pause_btn, resume_btn, stop_btn


def progress_section():
    """Sekcja postępu."""
    if st.session_state.running or st.session_state.results:
        st.header("📈 Postęp")
        
        progress = st.session_state.progress
        total = st.session_state.total
        
        if total > 0:
            st.progress(progress / total)
            st.write(f"Sprawdzono: {progress} / {total}")
        
        # Metryki
        results = st.session_state.results
        if results:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Sprawdzonych", len(results))
            
            with col2:
                found = sum(1 for r in results if r.get("found_on_allegro"))
                st.metric("Znalezionych", found)
            
            with col3:
                matching = sum(1 for r in results if r.get("matching_offers"))
                st.metric("Z pasującymi", matching)
            
            with col4:
                errors = sum(1 for r in results if r.get("status") == "error")
                st.metric("Błędów", errors)


def results_section():
    """Sekcja wyników."""
    if st.session_state.results:
        st.header("📋 Wyniki")
        
        results = st.session_state.results
        
        # Konwersja do DataFrame
        data = []
        for r in results:
            best = r.get("best_match")
            data.append({
                "EAN": r.get("ean"),
                "Moja cena": r.get("my_price"),
                "Nazwa": r.get("name", ""),
                "Znaleziono": "✅" if r.get("found_on_allegro") else "❌",
                "Cena Allegro": best.get("price") if best else None,
                "Kupujących": best.get("buyers_count") if best else None,
                "Status": r.get("status"),
            })
        
        df = pd.DataFrame(data)
        
        # Filtrowanie
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            show_only_matching = st.checkbox("Tylko z pasującymi ofertami")
        with filter_col2:
            show_only_found = st.checkbox("Tylko znalezione na Allegro")
        
        if show_only_matching:
            df = df[df["Kupujących"].notna()]
        if show_only_found:
            df = df[df["Znaleziono"] == "✅"]
        
        st.dataframe(df, use_container_width=True)
        
        # Export
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Zapisz JSON"):
                output_path = f"data/output/results_{datetime.now().strftime('%Y-%m-%d_%H%M')}.json"
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump({
                        "generated_at": datetime.now().isoformat(),
                        "products": results
                    }, f, ensure_ascii=False, indent=2)
                st.success(f"Zapisano: {output_path}")
        
        with col2:
            csv = df.to_csv(index=False, sep=";")
            st.download_button(
                "📥 Pobierz CSV",
                csv,
                f"results_{datetime.now().strftime('%Y-%m-%d')}.csv",
                "text/csv"
            )


def main():
    st.title("📊 Allegro Price Monitor")
    st.caption("Sprawdzanie cen i sprzedaży produktów na Allegro")
    
    init_session_state()
    sidebar_config()
    
    # Upload
    df = upload_section()
    
    # Szacowanie kosztów (jeśli wczytano plik)
    can_start = True
    if df is not None and len(df) > 0:
        can_start = cost_estimate_section(len(df))
    
    # Kontrola
    start_btn, pause_btn, resume_btn, stop_btn = control_section()
    
    if start_btn and df is not None and can_start:
        st.session_state.running = True
        st.session_state.results = []
        st.session_state.total = len(df)
        st.session_state.progress = 0
        
        # Odśwież kredyty po starcie
        refresh_credits_info()
        
        st.info("Przetwarzanie rozpoczęte... (odśwież stronę, aby zobaczyć postęp)")
    elif start_btn and not can_start:
        st.error("Nie można rozpocząć - za mało kredytów!")
    
    if stop_btn:
        st.session_state.running = False
        st.warning("Zatrzymano")
    
    # Postęp
    progress_section()
    
    # Wyniki
    results_section()
    
    # Statystyki sesji scrape.do
    client = get_scrape_client()
    if client and client.stats.total_requests > 0:
        st.sidebar.divider()
        st.sidebar.subheader("📊 Sesja")
        st.sidebar.caption(f"""
        Zapytań: {client.stats.total_requests}  
        Kredytów użyto: {client.stats.total_credits_used}  
        Ostatni koszt: {client.stats.last_request_cost}
        """)
    
    # Info
    st.sidebar.divider()
    st.sidebar.caption("""
    **Allegro Price Monitor**  
    Wersja 1.1
    
    Tryb konsolowy:
    ```
    python src/main.py run -i plik.csv -s scrape_do
    ```
    """)


if __name__ == "__main__":
    main()
