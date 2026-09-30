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
from src.api.scraper import ScrapeDoClient, ScraperError, search_allegro_by_ean


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
    if "paused" not in st.session_state:
        st.session_state.paused = False
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
    if "range_start" not in st.session_state:
        st.session_state.range_start = 1
    if "range_end" not in st.session_state:
        st.session_state.range_end = 100
    if "batch_size" not in st.session_state:
        st.session_state.batch_size = 100
    if "range_df_len" not in st.session_state:
        st.session_state.range_df_len = 0
    if "job_products" not in st.session_state:
        st.session_state.job_products = []
    if "job_index" not in st.session_state:
        st.session_state.job_index = 0
    if "current_ean" not in st.session_state:
        st.session_state.current_ean = None
    if "data_source" not in st.session_state:
        st.session_state.data_source = "scrape_do"


def _row_value(row: pd.Series, *keys: str) -> str:
    """Pobiera pierwszą niepustą wartość z wiersza po liście kluczy (case-insensitive)."""
    lower_map = {str(c).strip().lower(): c for c in row.index}
    for key in keys:
        col = key if key in row.index else lower_map.get(key.lower())
        if col is None:
            continue
        val = row[col]
        if pd.isna(val):
            continue
        text = str(val).strip()
        if text:
            return text
    return ""


def df_to_input_products(df: pd.DataFrame) -> list[InputProduct]:
    """Konwertuje DataFrame (Kod produktu/brutto lub ean/cena) na listę InputProduct."""
    products: list[InputProduct] = []
    for _, row in df.iterrows():
        code = _row_value(
            row,
            "Kod produktu",
            "ean",
            "EAN",
            "kod",
            "code",
        )
        if not code:
            continue

        price_raw = _row_value(
            row,
            "brutto",
            "cena",
            "price",
            "my_price",
        )
        try:
            price = float(price_raw.replace(",", ".").replace(" ", "")) if price_raw else 0.0
        except ValueError:
            price = 0.0

        name = _row_value(row, "nazwa", "name") or None
        products.append(InputProduct(ean=code, my_price=price, name=name))
    return products


def build_data_fetcher(source: str):
    """
    Tworzy data_fetcher dla ProductProcessor.
    scrape_do reuse'uje ScrapeDoClient z sesji (spójne kredyty).
    Zwraca None i pokazuje błąd przy braku konfiguracji.
    Błędy API są propagowane (status=error), nie maskowane jako pusta lista.
    """
    from src.core.request_log import log_request

    if source == "scrape_do":
        client = get_scrape_client()
        if client is None:
            st.error("Brak tokena scrape.do w .env — nie można uruchomić scrapowania.")
            return None

        def fetch_scrape(ean: str) -> list[dict]:
            offers = search_allegro_by_ean(ean, client, render=True)
            return [
                {
                    "offer_id": o.offer_id,
                    "title": o.title,
                    "price": o.price,
                    "currency": o.currency,
                    "seller_name": o.seller_name,
                    "buyers_count": o.buyers_count,
                    "url": o.url,
                    "is_smart": o.is_smart,
                }
                for o in offers
            ]

        return fetch_scrape

    if source == "api":
        try:
            allegro = AllegroClient()
            allegro.get_token()
        except Exception as e:
            st.error(f"API Allegro niedostępne: {e}")
            return None

        def fetch_api(ean: str) -> list[dict]:
            url = f"{allegro.API_URL}/offers/listing"
            try:
                result = allegro.search_offers(phrase=ean)
                items = result.get("items", {})
                offers = items.get("promoted", []) + items.get("regular", [])
                mapped = [
                    {
                        "offer_id": o.get("id", ""),
                        "title": o.get("name", ""),
                        "price": float(
                            o.get("sellingMode", {}).get("price", {}).get("amount", 0)
                        ),
                        "currency": o.get("sellingMode", {})
                        .get("price", {})
                        .get("currency", "PLN"),
                        "seller_name": o.get("seller", {}).get("login", ""),
                        "buyers_count": o.get("popularity", {}).get("soldCount"),
                        "url": f"https://allegro.pl/oferta/{o.get('id', '')}",
                        "is_smart": o.get("delivery", {}).get("smart", False),
                    }
                    for o in offers
                ]
                log_request(
                    source="api",
                    url=url,
                    code=ean,
                    http_status=200,
                    error=None,
                    response_text=json.dumps(result, ensure_ascii=False)[:4000],
                    offers_parsed=len(mapped),
                    offer_titles=[m["title"] for m in mapped if m.get("title")],
                    extra={"phrase": ean},
                    save_html_on_empty=False,
                )
                return mapped
            except AllegroAPIError as e:
                log_request(
                    source="api",
                    url=url,
                    code=ean,
                    http_status=e.status_code,
                    error=str(e),
                    response_text=None,
                    offers_parsed=0,
                    offer_titles=[],
                    extra={"code": e.code, "phrase": ean},
                    save_html_on_empty=False,
                )
                raise

        return fetch_api

    st.error(f"Nieznane źródło danych: {source}")
    return None


def _clamp_range(start: int, end: int, n_total: int) -> tuple[int, int]:
    """Przycina zakres 1-based do granic listy i wymusza od <= do."""
    if n_total <= 0:
        return 1, 1
    start = max(1, min(int(start), n_total))
    end = max(1, min(int(end), n_total))
    if start > end:
        start, end = end, start
    return start, end


def _apply_range(start: int, end: int, n_total: int) -> None:
    """Ustawia range_start / range_end w session_state."""
    start, end = _clamp_range(start, end, n_total)
    st.session_state.range_start = start
    st.session_state.range_end = end


def _on_range_preset_change() -> None:
    """Callback: aplikuje wybrany preset zakresu."""
    preset = st.session_state.get("range_preset")
    n_total = st.session_state.get("range_df_len", 0)
    if not preset or n_total <= 0:
        return

    batch_size = int(st.session_state.get("batch_size", 100))
    can_process = st.session_state.get("range_can_process")

    if preset == "Pierwsze 5":
        _apply_range(1, 5, n_total)
    elif preset == "Pierwsze 10":
        _apply_range(1, 10, n_total)
    elif preset == "10–15 (test)":
        _apply_range(10, 15, n_total)
    elif preset == "Pierwsze 100":
        _apply_range(1, 100, n_total)
    elif preset == "Według partii":
        _apply_range(1, batch_size, n_total)
    elif preset == "Max wg kredytów":
        limit = can_process if can_process is not None else n_total
        _apply_range(1, max(1, int(limit)), n_total)


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
    source_options = ["scrape_do", "api"]
    current = st.session_state.get("data_source", "scrape_do")
    if current not in source_options:
        current = "scrape_do"
    source = st.sidebar.selectbox(
        "Wybierz źródło",
        source_options,
        index=source_options.index(current),
        help="scrape_do = listing jak w przeglądarce; api = API Allegro (wymaga weryfikacji)",
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

    # Logi zapytań
    from src.core.request_log import get_last_log, logs_dir

    st.sidebar.divider()
    st.sidebar.subheader("📋 Logi zapytań")
    st.sidebar.caption(f"Katalog: `{logs_dir()}`")
    last = get_last_log()
    if last:
        st.sidebar.caption(
            f"Ostatnie: `{last.get('code')}` · oferty={last.get('offers_parsed')} · "
            f"status={last.get('http_status')} · err={last.get('error') or '—'}"
        )
        st.sidebar.caption(f"Plik: `{last.get('path')}`")
    else:
        st.sidebar.caption("Brak logów w tej sesji.")
    
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
            st.dataframe(df.head(10), width="stretch")
            st.session_state.input_df = df
            return df
        except Exception as e:
            st.error(f"Błąd wczytywania: {e}")
    
    return None


def _on_range_bounds_change() -> None:
    """Callback: utrzymaj od <= do w granicach listy."""
    n_total = st.session_state.get("range_df_len", 0)
    if n_total <= 0:
        return
    start, end = _clamp_range(
        st.session_state.range_start,
        st.session_state.range_end,
        n_total,
    )
    st.session_state.range_start = start
    st.session_state.range_end = end


def _on_next_batch() -> None:
    """Callback: przesuń zakres o rozmiar partii do przodu."""
    n_total = st.session_state.get("range_df_len", 0)
    if n_total <= 0:
        return
    next_start = int(st.session_state.range_end) + 1
    if next_start > n_total:
        return
    batch = int(st.session_state.get("batch_size", 100))
    _apply_range(next_start, next_start + batch - 1, n_total)
    st.session_state.range_preset = None


def range_section(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sekcja wyboru zakresu wierszy do scrapowania.
    Numeracja 1-based (jak w Excelu). Zwraca wycinek DataFrame.
    """
    st.subheader("Zakres produktów")
    n_total = len(df)

    # Reset zakresu przy nowym / innym pliku — domyślnie pierwsze 100
    if st.session_state.range_df_len != n_total:
        st.session_state.range_df_len = n_total
        _apply_range(1, min(100, n_total), n_total)
        st.session_state.range_preset = None

    # Ile maksymalnie pozwala saldo kredytów (dla presetu)
    can_process = None
    client = get_scrape_client()
    if client:
        if st.session_state.credits_info is None:
            refresh_credits_info()
        # Utrzymaj stats klienta zsynchronizowane z cache w sesji
        info = st.session_state.credits_info
        if info and "error" not in info:
            remaining = info.get("RemainingMonthlyRequest")
            if remaining is not None:
                client.stats.remaining_credits = remaining
            max_monthly = info.get("MaxMonthlyRequest")
            if max_monthly is not None:
                client.stats.max_monthly_credits = max_monthly
        estimate = client.estimate_cost(1, render=True)
        can_process = estimate.get("can_process")
    st.session_state.range_can_process = can_process

    st.pills(
        "Presety",
        options=[
            "Pierwsze 5",
            "Pierwsze 10",
            "10–15 (test)",
            "Pierwsze 100",
            "Według partii",
            "Max wg kredytów",
        ],
        key="range_preset",
        on_change=_on_range_preset_change,
        help="Szybkie zaznaczenie zakresu. „Według partii” = pierwsze N wg rozmiaru partii poniżej.",
    )

    col_from, col_to, col_batch = st.columns(3)
    with col_from:
        st.number_input(
            "Od wiersza",
            min_value=1,
            max_value=max(n_total, 1),
            step=1,
            key="range_start",
            on_change=_on_range_bounds_change,
        )
    with col_to:
        st.number_input(
            "Do wiersza",
            min_value=1,
            max_value=max(n_total, 1),
            step=1,
            key="range_end",
            on_change=_on_range_bounds_change,
        )
    with col_batch:
        st.number_input(
            "Rozmiar partii",
            min_value=1,
            max_value=1000,
            step=1,
            key="batch_size",
            help="Używane przez preset „Według partii” i przycisk „Kolejna partia”.",
        )

    start, end = _clamp_range(
        st.session_state.range_start,
        st.session_state.range_end,
        n_total,
    )
    selected_count = end - start + 1
    st.caption(f"Wybrane: wiersze {start}–{end} ({selected_count} z {n_total})")

    next_start = end + 1
    can_next = next_start <= n_total and not st.session_state.running
    st.button(
        ":material/skip_next: Kolejna partia",
        disabled=not can_next,
        on_click=_on_next_batch,
        help=(
            f"Przesuwa zakres o rozmiar partii ({st.session_state.batch_size}) "
            "do przodu — osobno od Pauza/Wznów."
            if can_next
            else "Brak kolejnych wierszy lub trwa przetwarzanie."
        ),
    )

    selected_df = df.iloc[start - 1 : end].copy()
    with st.expander("Podgląd wybranego zakresu", expanded=selected_count <= 20):
        st.dataframe(selected_df, width="stretch")

    return selected_df


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

    running = st.session_state.running
    paused = st.session_state.paused

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        start_btn = st.button("▶️ Start", disabled=running)
    with col2:
        pause_btn = st.button("⏸️ Pauza", disabled=not running or paused)
    with col3:
        resume_btn = st.button("▶️ Wznów", disabled=not running or not paused)
    with col4:
        stop_btn = st.button("⏹️ Stop", disabled=not running)

    return start_btn, pause_btn, resume_btn, stop_btn


def progress_section():
    """Sekcja postępu."""
    if not (st.session_state.running or st.session_state.results):
        return

    st.header("📈 Postęp")

    progress = st.session_state.progress
    total = st.session_state.total

    if total > 0:
        st.progress(min(progress / total, 1.0))
        st.write(f"Sprawdzono: {progress} / {total}")

    if st.session_state.running and st.session_state.paused:
        st.warning("Wstrzymano — kliknij Wznów, aby kontynuować.")
    elif st.session_state.running:
        products = st.session_state.job_products
        idx = st.session_state.job_index
        if products and idx < len(products):
            st.info(f"Sprawdzam: `{products[idx].ean}`")
        elif st.session_state.current_ean:
            st.info(f"Sprawdzam: `{st.session_state.current_ean}`")

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
                "Cache": "tak" if r.get("from_cache") else "",
                "Błąd": r.get("error_message") or "",
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
        
        st.dataframe(df, width="stretch")
        
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


def _stop_job() -> None:
    """Zatrzymuje bieżące zadanie i czyści kolejkę."""
    st.session_state.running = False
    st.session_state.paused = False
    st.session_state.current_ean = None
    st.session_state.job_products = []
    st.session_state.job_index = 0
    processor = st.session_state.processor
    if processor is not None:
        processor.stop()


def process_job_tick() -> None:
    """
    Przetwarza jeden produkt z kolejki (jeden krok na rerun).
    Wywoływać po sekcji postępu, gdy running and not paused.
    """
    if not st.session_state.running or st.session_state.paused:
        return

    products: list[InputProduct] = st.session_state.job_products
    idx = st.session_state.job_index
    processor: ProductProcessor | None = st.session_state.processor

    if not products or processor is None:
        _stop_job()
        st.error("Brak kolejki produktów lub procesora — zatrzymano.")
        return

    if idx >= len(products):
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.current_ean = None
        refresh_credits_info()
        st.success(f"Zakończono — sprawdzono {len(st.session_state.results)} produktów.")
        return

    product = products[idx]
    st.session_state.current_ean = product.ean
    st.caption(f"Pobieranie danych dla `{product.ean}`…")

    result = processor.process_single(product)
    st.session_state.results.append(result.to_dict())
    st.session_state.job_index = idx + 1
    st.session_state.progress = idx + 1

    if st.session_state.job_index >= len(products):
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.current_ean = None
        refresh_credits_info()
        st.success(f"Zakończono — sprawdzono {len(st.session_state.results)} produktów.")
        st.rerun()
        return

    delay = float(st.session_state.config.delay_seconds)
    time.sleep(delay)
    st.rerun()


def main():
    st.title("📊 Allegro Price Monitor")
    st.caption("Sprawdzanie cen i sprzedaży produktów na Allegro")

    init_session_state()
    sidebar_config()

    df = upload_section()

    can_start = True
    selected_df = None
    if df is not None and len(df) > 0:
        selected_df = range_section(df)
        if st.session_state.data_source == "scrape_do":
            can_start = cost_estimate_section(len(selected_df))
        else:
            cost_estimate_section(len(selected_df))

    start_btn, pause_btn, resume_btn, stop_btn = control_section()

    if start_btn and selected_df is not None and can_start:
        products = df_to_input_products(selected_df)
        if not products:
            st.error("Brak produktów z kodem w wybranym zakresie.")
        else:
            source = st.session_state.get("data_source", "scrape_do")
            fetcher = build_data_fetcher(source)
            if fetcher is not None:
                st.session_state.processor = ProductProcessor(
                    config=st.session_state.config,
                    data_fetcher=fetcher,
                )
                st.session_state.job_products = products
                st.session_state.job_index = 0
                st.session_state.results = []
                st.session_state.total = len(products)
                st.session_state.progress = 0
                st.session_state.current_ean = None
                st.session_state.paused = False
                st.session_state.running = True
                st.session_state.selected_df = selected_df
                if source == "scrape_do":
                    refresh_credits_info()
                st.info(
                    f"Przetwarzanie wierszy "
                    f"{st.session_state.range_start}–{st.session_state.range_end} "
                    f"({len(products)} produktów, źródło: `{source}`)."
                )
    elif start_btn and selected_df is None:
        st.error("Najpierw wczytaj plik CSV.")
    elif start_btn and not can_start:
        st.error("Nie można rozpocząć - za mało kredytów na wybrany zakres!")

    if pause_btn and st.session_state.running:
        st.session_state.paused = True
        processor = st.session_state.processor
        if processor is not None:
            processor.pause()

    if resume_btn and st.session_state.running and st.session_state.paused:
        st.session_state.paused = False
        processor = st.session_state.processor
        if processor is not None:
            processor.resume()
        st.rerun()

    if stop_btn:
        _stop_job()
        st.warning("Zatrzymano")

    progress_section()
    results_section()
    process_job_tick()

    client = get_scrape_client()
    if client and client.stats.total_requests > 0:
        st.sidebar.divider()
        st.sidebar.subheader("📊 Sesja")
        st.sidebar.caption(f"""
        Zapytań: {client.stats.total_requests}  
        Kredytów użyto: {client.stats.total_credits_used}  
        Ostatni koszt: {client.stats.last_request_cost}
        """)

    st.sidebar.divider()
    st.sidebar.caption("""
    **Allegro Price Monitor**  
    Wersja 1.2
    
    Tryb konsolowy:
    ```
    python src/main.py run -i plik.csv -s scrape_do
    ```
    """)


if __name__ == "__main__":
    main()
