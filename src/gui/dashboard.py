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

# Dodaj sciezke
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd

from src.core.processor import ProductProcessor, ProcessorConfig, InputProduct, ProductResult
from src.core.cache import ProductCache
from src.api.allegro import AllegroClient, AllegroAPIError


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
    
    # Kontrola
    start_btn, pause_btn, resume_btn, stop_btn = control_section()
    
    if start_btn and df is not None:
        st.session_state.running = True
        st.session_state.results = []
        st.session_state.total = len(df)
        st.session_state.progress = 0
        st.info("Przetwarzanie rozpoczęte... (odśwież stronę, aby zobaczyć postęp)")
    
    if stop_btn:
        st.session_state.running = False
        st.warning("Zatrzymano")
    
    # Postęp
    progress_section()
    
    # Wyniki
    results_section()
    
    # Info
    st.sidebar.divider()
    st.sidebar.caption("""
    **Allegro Price Monitor**  
    Wersja 1.0
    
    Tryb konsolowy:
    ```
    python src/main.py run -i plik.csv
    ```
    """)


if __name__ == "__main__":
    main()
