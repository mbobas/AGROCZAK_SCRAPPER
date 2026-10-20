"""
GUI Dashboard - Streamlit interface.
Uruchom: streamlit run src/gui/dashboard.py
"""
import os
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

import requests
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from src.core.processor import ProductProcessor, ProcessorConfig, InputProduct, ProductResult
from src.core.cache import ProductCache
from src.api.scraper import ScrapeDoClient, search_allegro_by_ean

load_dotenv()

st.set_page_config(
    page_title="Allegro Price Monitor",
    page_icon="📊",
    layout="wide"
)

CLOUD_APP_HOST = "agroczakscrapper-5nmik62ymzukf8hpefafsn.streamlit.app"
AUTH_WEBHOOK_URL = (
    "https://marcin286-20286.wykr.es/webhook/68fe834b-69fc-4ee4-8170-f443b66caa1e"
)
AUTH_REQUEST_TIMEOUT_S = 15


def _request_host() -> str:
    """Host z nagłówków HTTP Streamlit (bez portu)."""
    try:
        headers = st.context.headers
    except Exception:
        return ""
    raw = headers.get("Host") or headers.get("host") or ""
    return str(raw).split(":")[0].strip().lower()


def _app_mode_override() -> str:
    """APP_MODE z secrets lub env (np. analyze_only do testów lokalnych)."""
    try:
        mode = st.secrets.get("APP_MODE")
        if mode:
            return str(mode).strip().lower()
    except Exception:
        pass
    return os.getenv("APP_MODE", "").strip().lower()


def is_analyze_only() -> bool:
    """True na Streamlit Cloud (*.streamlit.app) lub gdy APP_MODE=analyze_only."""
    mode = _app_mode_override()
    if mode in {"analyze_only", "analyze", "cloud"}:
        return True
    host = _request_host()
    if not host:
        return False
    if host == CLOUD_APP_HOST or host.endswith(".streamlit.app"):
        return True
    return False


def verify_password(password: str) -> tuple[bool, str]:
    """
    Weryfikuje hasło przez POST na webhook n8n.
    Sukces = HTTP 200. Hasło idzie jako query param `password`.
    """
    password = (password or "").strip()
    if not password:
        return False, "Podaj hasło."

    try:
        response = requests.post(
            AUTH_WEBHOOK_URL,
            params={"password": password},
            timeout=AUTH_REQUEST_TIMEOUT_S,
            verify=False,
        )
    except requests.RequestException as exc:
        return False, f"Błąd połączenia z weryfikacją: {exc}"

    if response.status_code == 200:
        return True, ""
    return False, "Nieprawidłowe hasło."


def require_login() -> bool:
    """
    Bramka wejścia: pokazuje formularz hasła, dopóki sesja nie jest uwierzytelniona.
    Zwraca True gdy użytkownik może korzystać z aplikacji.
    """
    if st.session_state.get("authenticated"):
        return True

    st.title("Allegro Price Monitor")
    st.caption("Aby wejść, podaj hasło dostępu.")

    with st.form("login_form", clear_on_submit=False):
        password = st.text_input("Hasło", type="password", autocomplete="current-password")
        submitted = st.form_submit_button("Zaloguj", type="primary", use_container_width=True)

    if submitted:
        ok, message = verify_password(password)
        if ok:
            st.session_state.authenticated = True
            st.rerun()
        st.error(message or "Nieprawidłowe hasło.")

    return False


def init_session_state():
    """Inicjalizuje stan sesji."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
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
    st.session_state.data_source = "scrape_do"
    if "search_mode" not in st.session_state:
        st.session_state.search_mode = "Kod"
    if "use_render" not in st.session_state:
        st.session_state.use_render = False
    if "last_autosave_path" not in st.session_state:
        st.session_state.last_autosave_path = None
    if "analyze_products" not in st.session_state:
        st.session_state.analyze_products = []
    if "analyze_source_label" not in st.session_state:
        st.session_state.analyze_source_label = None


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


def build_data_fetcher():
    """
    Tworzy data_fetcher przez scrape.do (jedyny tryb).
    Reuse'uje ScrapeDoClient z sesji (spójne kredyty).
    Render bierze z st.session_state.use_render.
    """
    client = get_scrape_client()
    if client is None:
        st.error("Brak tokena scrape.do w .env — nie można uruchomić scrapowania.")
        return None

    render = bool(st.session_state.get("use_render", False))

    def fetch_scrape(query: str) -> list[dict]:
        # query = kod produktu (tryb Kod) albo fraza z nazwy (tryb Nazwa)
        offers = search_allegro_by_ean(query, client, render=render)
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
    
    st.sidebar.subheader("Źródło danych")
    st.sidebar.caption("Zablokowane: **scrape.do** (listing Allegro jak w przeglądarce).")
    st.session_state.data_source = "scrape_do"

    st.sidebar.toggle(
        "Render JS (headless)",
        key="use_render",
        help="OFF (domyślnie) ≈ 1 kred./zapytanie. ON ≈ 5 kred./zapytanie (pełniejszy listing).",
    )
    if st.session_state.use_render:
        st.sidebar.caption("~5 kred./zapytanie — pełniejszy listing.")
    else:
        st.sidebar.warning(
            "Bez renderu taniej (~1 kred.), ale Allegro może zwrócić mniej ofert "
            "albo bez liczby kupujących; czasem 0 wyników mimo że na stronie coś jest."
        )

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
            
            # Koszty — aktywny tryb
            active = st.session_state.get("use_render", False)
            if active:
                st.sidebar.caption("**Aktywny tryb:** render ON → ~5 kred./zapytanie")
            else:
                st.sidebar.caption("**Aktywny tryb:** render OFF → ~1 kred./zapytanie")
            st.sidebar.caption(
                "Cennik: render=true = 5 kred. · render=false = 1 kred."
            )
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
            try:
                df = pd.read_csv(uploaded_file, sep=";")
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, sep=";", encoding="cp1250")
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
        use_render = bool(st.session_state.get("use_render", False))
        estimate = client.estimate_cost(1, render=use_render)
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

    use_render = bool(st.session_state.get("use_render", False))
    estimate = client.estimate_cost(num_products, render=use_render)
    cost_per = estimate.get("cost_per_request", 5 if use_render else 1)
    st.caption(
        f"Tryb: render={'ON' if use_render else 'OFF'} "
        f"(~{cost_per} kred./produkt)"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Produktów", num_products)

    with col2:
        st.metric("Koszt (kredyty)", estimate['total_cost'])

    with col3:
        remaining = estimate['remaining_credits']
        if remaining is not None:
            st.metric("Pozostanie", remaining - estimate['total_cost'])

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
        from src.core.results_io import count_matching_offers

        cfg = st.session_state.config
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Sprawdzonych", len(results))
        with col2:
            found = sum(1 for r in results if r.get("found_on_allegro"))
            st.metric("Znalezionych", found)
        with col3:
            matching = sum(
                1
                for r in results
                if count_matching_offers(
                    r,
                    min_markup=cfg.min_markup,
                    max_markup=cfg.max_markup,
                    min_buyers=cfg.min_buyers,
                )
            )
            st.metric("Z pasującymi", matching)
        with col4:
            errors = sum(1 for r in results if r.get("status") == "error")
            st.metric("Błędów", errors)


def results_columns_help(*, key: str = "results_columns_help") -> None:
    """Pytajnik z objaśnieniem kolumn tabeli wyników."""
    with st.popover(":material/help: Znaczenie kolumn"):
        st.markdown(
            """
**Status**
- ✅ **checked** — sprawdzenie się udało (scrape/API OK). *Nie* znaczy „pasuje cenowo”.
- ❌ **error** — błąd zapytania (API, scrape.do, sieć); treść w kolumnie **Błąd**.
- ⏳ **pending** — jeszcze nie sprawdzone.

**Pasujące** — liczone na żywo wg filtrów (sidebar): marża min–max względem Twojej ceny
oraz min. kupujących. Przy domyślnych 0–50% i min. kupujących = 0 zwykle = wszystkie oferty.
Gdy zacieśnisz filtry, liczba spada. Min. kupujących = 0 → oferty bez `buyers_count` też liczą się.

**Błąd** — puste = OK. Komunikat tylko przy statusie error.

**Marża min %** — ile % drożej jest *najtańsza* oferta Allegro względem **Moja cena**:
`(cena_min / moja_cena − 1) × 100`.

**Nazwa** — nazwa produktu z pliku wejściowego (kolumna `nazwa`).

**Dopasowanie % / Dopasowanie max %** — jaki procent znaczących słów z Twojej nazwy
(bez słów typu „oryginał”, „do”) występuje w tytule oferty Allegro; w podsumowaniu
najlepszy wynik spośród ofert. Np. 3 z 4 słów = 75%. Odmiana słów i polskie znaki
są tolerowane; numery katalogowe muszą się zgadzać dokładnie.
**100%** tylko gdy kod produktu jest w tytule i pasuje choć jedno słowo z nazwy;
sama nazwa daje max 99%, sam kod (bez słów z nazwy) 90%.

**Znaleziono** — czy listing zwrócił jakiekolwiek oferty (niezależnie od filtrów).

**Liczba ofert / Cena min–max** — po deduplikacji `offer_id` z listingu.
            """
        )


def results_section():
    """Sekcja wyników scrapowania — podsumowanie ofert + ekspandery."""
    from src.core.results_io import (
        save_results_json,
        summary_row,
        offer_stats,
        offer_match_pct,
    )

    if not st.session_state.results:
        return

    head_l, head_r = st.columns([4, 1])
    with head_l:
        st.header("Wyniki")
    with head_r:
        results_columns_help(key="scrape_results_help")

    results = st.session_state.results
    cfg = st.session_state.config
    filter_kw = dict(
        min_markup=cfg.min_markup,
        max_markup=cfg.max_markup,
        min_buyers=cfg.min_buyers,
    )

    rows = [summary_row(r, **filter_kw) for r in results]
    df = pd.DataFrame(rows)

    st.caption(
        f"Pasujące wg sidebara: marża {cfg.min_markup*100:.0f}–{cfg.max_markup*100:.0f}%, "
        f"min. kupujących = {cfg.min_buyers} "
        f"(zmiana filtrów odświeża kolumnę bez ponownego scrapu)."
    )

    from src.core.matching import match_legend_text

    st.caption("Legenda dopasowania: " + match_legend_text())

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        show_only_matching = st.checkbox(
            "Tylko z pasującymi (wg filtrów sidebara)",
            key="scrape_only_matching",
            help="Pokazuje wiersze, gdzie Pasujące > 0 (aktualne filtry marży i kupujących).",
        )
    with filter_col2:
        show_only_found = st.checkbox(
            "Tylko znalezione na Allegro",
            key="scrape_only_found",
            help="Ukrywa produkty bez żadnej oferty na listingu.",
        )

    view = df
    if show_only_matching:
        view = view[view["Pasujące"] > 0]
    if show_only_found:
        view = view[view["Znaleziono"].astype(str).str.contains("tak", case=False, na=False)]

    st.dataframe(view, width="stretch")

    with st.expander("Szczegóły ofert (wszystkie ceny)", expanded=False):
        for r in results:
            stats = offer_stats(r, **filter_kw)
            code = r.get("ean")
            st.markdown(
                f"**`{code}`** — ofert: {stats['offers_count']}, "
                f"pasujących: {stats['matching_count']}, "
                f"cena {stats['min_price']}–{stats['max_price']}"
            )
            if stats["offers"]:
                offers_df = pd.DataFrame(
                    [
                        {
                            "Nazwa": r.get("name"),
                            "Moja cena": r.get("my_price"),
                            "Dopasowanie %": offer_match_pct(r, o),
                            "Tytuł": o.get("title"),
                            "Cena": o.get("price"),
                            "Sprzedawca": o.get("seller_name"),
                            "Kupujących": o.get("buyers_count"),
                            "URL": o.get("url"),
                        }
                        for o in stats["offers"]
                    ]
                )
                st.dataframe(offers_df, width="stretch")
            else:
                st.caption("Brak ofert.")

    if st.session_state.last_autosave_path:
        st.success(f"Ostatni autozapis: `{st.session_state.last_autosave_path}`")

    st.caption(
        "Autozapis po zakończeniu scrapowania: `data/output/` "
        "(`results_DATA_szukanie_po_kodzie|nazwie.json`). "
        "Ręczne zapisywanie nadal dostępne."
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zapisz wyniki JSON (pełne oferty)", key="manual_save_json"):
            mode = (
                "name" if st.session_state.search_mode == "Nazwa" else "code"
            )
            path = save_results_json(results, search_mode=mode)
            st.success(f"Zapisano: {path}")
    with col2:
        csv = view.to_csv(index=False, sep=";")
        st.download_button(
            "Pobierz CSV (podsumowanie)",
            csv,
            f"results_summary_{datetime.now().strftime('%Y-%m-%d')}.csv",
            "text/csv",
            key="manual_download_csv",
            help="CSV = tabela podsumowania. Pełne oferty są w JSON.",
        )


def analyze_section():
    """Zakładka: wczytaj JSON wyników i filtruj lokalnie (bez kredytów)."""
    from src.core.matching import match_legend_text
    from src.core.results_io import (
        analyzer_summary_row,
        filter_products,
        flatten_offers,
        list_result_files,
        load_results_json,
        save_results_json,
    )

    st.header("Analiza wyników")
    st.caption(
        "Wczytaj zapisany JSON i filtruj lokalnie — bez ponownego scrapowania / kredytów."
    )

    files = list_result_files()
    file_labels = [f.name for f in files]
    source_mode = st.radio(
        "Źródło danych",
        ["Plik z data/output", "Upload JSON"],
        horizontal=True,
        key="analyze_source_mode",
    )

    if source_mode == "Plik z data/output":
        if not file_labels:
            st.info("Brak plików w `data/output/`. Najpierw uruchom scrapowanie.")
        else:
            choice = st.selectbox(
                "Wybierz plik wyników", file_labels, key="analyze_file_pick"
            )
            if st.button("Wczytaj wybrany plik", key="analyze_load_file"):
                path = next(f for f in files if f.name == choice)
                st.session_state.analyze_products = load_results_json(path)
                st.session_state.analyze_source_label = str(path)
                st.rerun()
    else:
        uploaded = st.file_uploader(
            "Wgraj results_*.json",
            type=["json"],
            key="analyze_upload",
        )
        if uploaded is not None and st.button(
            "Wczytaj upload", key="analyze_load_upload"
        ):
            raw = json.loads(uploaded.getvalue().decode("utf-8"))
            if isinstance(raw, dict):
                st.session_state.analyze_products = list(raw.get("products") or [])
            else:
                st.session_state.analyze_products = list(raw or [])
            st.session_state.analyze_source_label = uploaded.name
            st.rerun()

    products = st.session_state.analyze_products or []
    if st.session_state.analyze_source_label:
        st.caption(
            f"Wczytano: `{st.session_state.analyze_source_label}` "
            f"({len(products)} produktów)"
        )

    if not products:
        return

    st.subheader("Filtry lokalne")
    c1, c2 = st.columns(2)
    with c1:
        markup_range = st.select_slider(
            "Zakres marży % (względem mojej ceny)",
            options=list(range(-110, 111)),
            value=(0, 50),
            format_func=lambda v: (
                "-∞" if v <= -110 else "+∞" if v >= 110 else f"{v}%"
            ),
            key="analyze_markup_range",
            help="Skrajne położenia (-∞ / +∞) oznaczają brak ograniczenia z danej strony.",
        )
        min_offers = st.number_input(
            "Min. liczba ofert",
            min_value=0,
            max_value=100,
            value=1,
            key="analyze_min_offers",
        )
    with c2:
        require_offers = st.checkbox(
            "Tylko z co najmniej jedną ofertą",
            value=True,
            key="analyze_require_offers",
        )
        min_buyers = st.number_input(
            "Min. kupujących",
            min_value=0,
            max_value=1000,
            value=0,
            key="analyze_min_buyers",
            help=(
                "0 = bez filtra (oferty bez danych o kupujących też są widoczne). "
                "Od 1 w górę ukrywa oferty poniżej progu oraz oferty bez danych."
            ),
        )

    has_names = any((p.get("name") or "").strip() for p in products)
    min_match = st.slider(
        "Min. dopasowanie nazwy (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=5,
        key="analyze_min_match",
        disabled=not has_names,
        help=(
            "Udział słów z Twojej nazwy znalezionych w tytule oferty. "
            "Oferty poniżej progu są ukrywane."
            if has_names
            else "Wczytane wyniki nie zawierają nazw produktów (stary format pliku)."
        ),
    )
    if not has_names:
        min_match = 0
    st.caption("Legenda dopasowania: " + match_legend_text())

    m_lo = None if markup_range[0] <= -110 else float(markup_range[0])
    m_hi = None if markup_range[1] >= 110 else float(markup_range[1])
    buyers_f = int(min_buyers) if min_buyers > 0 else None
    offer_filters = dict(
        markup_min_pct=m_lo,
        markup_max_pct=m_hi,
        min_buyers=buyers_f,
        min_match_pct=float(min_match),
    )

    filtered = filter_products(
        products,
        min_offers=int(min_offers),
        require_offers=require_offers,
        **offer_filters,
    )

    st.metric("Po filtrach", f"{len(filtered)} / {len(products)}")

    a_l, a_r = st.columns([4, 1])
    with a_l:
        st.subheader("Podsumowanie")
    with a_r:
        results_columns_help(key="analyze_results_help")

    summary_df = pd.DataFrame(
        [
            analyzer_summary_row(p, **offer_filters)
            for p in filtered
        ]
    )
    st.dataframe(summary_df, width="stretch")

    flat = flatten_offers(filtered, **offer_filters)
    with st.expander(f"Oferty spłaszczone ({len(flat)})", expanded=True):
        if flat:
            st.dataframe(pd.DataFrame(flat), width="stretch")
        else:
            st.caption("Brak ofert po filtrach.")

    st.subheader("Eksport przefiltrowanych")
    ec1, ec2 = st.columns(2)
    with ec1:
        if st.button(
            "Zapisz przefiltrowane JSON",
            key="analyze_save_json",
            help=(
                "Zapisuje do data/output/ pełny format wyników (jak po scrapowaniu). "
                "Tylko produkty przechodzące filtry; u każdego zostaje pełna lista ofert "
                "(nie tylko te widoczne po filtrach). Da się znowu wczytać w Analizie. "
                "Nie ściąga pliku do przeglądarki."
            ),
        ):
            path = save_results_json(filtered)
            st.success(f"Zapisano: {path}")
    with ec2:
        if flat:
            st.download_button(
                "Pobierz oferty CSV",
                pd.DataFrame(flat).to_csv(index=False, sep=";"),
                f"offers_filtered_{datetime.now().strftime('%Y-%m-%d')}.csv",
                "text/csv",
                key="analyze_download_csv",
                help=(
                    "Pobiera tabelę „Oferty spłaszczone”: jedna oferta = jeden wiersz, "
                    "tylko oferty spełniające bieżące filtry (marża, kupujący, dopasowanie)."
                ),
            )
        st.download_button(
            "Pobierz podsumowanie CSV",
            summary_df.to_csv(index=False, sep=";"),
            f"summary_filtered_{datetime.now().strftime('%Y-%m-%d')}.csv",
            "text/csv",
            key="analyze_download_summary",
            help=(
                "Pobiera tabelę „Podsumowanie”: jeden produkt = jeden wiersz "
                "(liczba ofert, cena min/max itd. liczone po bieżących filtrach)."
            ),
        )


def _autosave_and_notify() -> None:
    """Zapisuje results z suffixem trybu szukania po zakończeniu joba."""
    from src.core.results_io import autosave_results

    results = st.session_state.results or []
    if not results:
        return
    mode = "name" if st.session_state.search_mode == "Nazwa" else "code"
    stamped = autosave_results(results, search_mode=mode)
    st.session_state.last_autosave_path = str(stamped)
    st.success(
        f"Zakończono — sprawdzono {len(results)} produktów. "
        f"Autozapis: `{stamped}`."
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
        _autosave_and_notify()
        return

    product = products[idx]
    st.session_state.current_ean = product.ean
    st.caption(f"Pobieranie danych dla `{product.ean}`…")

    processor.config = st.session_state.config
    result = processor.process_single(product)
    st.session_state.results.append(result.to_dict())
    st.session_state.job_index = idx + 1
    st.session_state.progress = idx + 1

    if st.session_state.job_index >= len(products):
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.current_ean = None
        refresh_credits_info()
        _autosave_and_notify()
        st.rerun()
        return

    delay = float(st.session_state.config.delay_seconds)
    time.sleep(delay)
    st.rerun()


def scrape_tab() -> None:
    """Zawartość zakładki Scrapowanie."""
    df = upload_section()

    can_start = True
    selected_df = None
    st.segmented_control(
        "Szukaj po",
        options=["Kod", "Nazwa"],
        key="search_mode",
        selection_mode="single",
        disabled=bool(st.session_state.running),
        help="Kod = fraza to kod produktu. Nazwa = fraza zbudowana z kolumny `nazwa`. "
        "Brak zaznaczenia = Kod.",
    )
    by_name = st.session_state.search_mode == "Nazwa"
    if by_name:
        st.info(
            "Tryb **Nazwa**: wyszukiwana jest nazwa z kolumny `nazwa` "
            "(bez słów typu „oryginał”). Dopasowanie % policzysz w Analizie wyników."
        )

    if df is not None and len(df) > 0:
        selected_df = range_section(df)
        can_start = cost_estimate_section(len(selected_df))
        if by_name:
            has_name_col = any(str(c).strip().lower() in ("nazwa", "name") for c in df.columns)
            if not has_name_col:
                st.error("Plik nie ma kolumny `nazwa` — nie można szukać po nazwie.")
                can_start = False

    start_btn, pause_btn, resume_btn, stop_btn = control_section()

    if start_btn and selected_df is not None and can_start:
        products = df_to_input_products(selected_df)
        if by_name:
            skipped = sum(1 for p in products if not (p.name or "").strip())
            products = [p for p in products if (p.name or "").strip()]
            if skipped:
                st.warning(f"Pominięto {skipped} produktów bez nazwy.")
        if not products:
            st.error("Brak produktów z kodem (i nazwą w trybie Nazwa) w wybranym zakresie.")
        else:
            fetcher = build_data_fetcher()
            if fetcher is not None:
                st.session_state.processor = ProductProcessor(
                    config=st.session_state.config,
                    data_fetcher=fetcher,
                    search_mode=(
                        "name" if st.session_state.search_mode == "Nazwa" else "code"
                    ),
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
                st.session_state.last_autosave_path = None
                refresh_credits_info()
                render_label = "on" if st.session_state.get("use_render", False) else "off"
                st.info(
                    f"Przetwarzanie wierszy "
                    f"{st.session_state.range_start}–{st.session_state.range_end} "
                    f"({len(products)} produktów, źródło: scrape.do, render={render_label})."
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


def main():
    init_session_state()

    if not require_login():
        return

    if is_analyze_only():
        st.title("Allegro Price Monitor")
        st.caption(
            "Tryb chmury: tylko analiza wyników (bez scrapowania / kredytów). "
            "Wgraj plik `results_*.json` z lokalnego uruchomienia."
        )
        analyze_section()
        st.sidebar.caption(
            "**Allegro Price Monitor**  \n"
            "Wersja 1.3 · tryb: analyze-only"
        )
        if st.sidebar.button("Wyloguj"):
            st.session_state.authenticated = False
            st.rerun()
        return

    st.title("Allegro Price Monitor")
    st.caption("Sprawdzanie cen i sprzedaży produktów na Allegro")

    sidebar_config()

    tab_scrape, tab_analyze = st.tabs(["Scrapowanie", "Analiza wyników"])
    with tab_scrape:
        scrape_tab()
    with tab_analyze:
        analyze_section()

    client = get_scrape_client()
    if client and client.stats.total_requests > 0:
        st.sidebar.divider()
        st.sidebar.subheader("Sesja")
        st.sidebar.caption(f"""
        Zapytań: {client.stats.total_requests}  
        Kredytów użyto: {client.stats.total_credits_used}  
        Ostatni koszt: {client.stats.last_request_cost}
        """)

    st.sidebar.divider()
    if st.sidebar.button("Wyloguj"):
        st.session_state.authenticated = False
        st.rerun()
    st.sidebar.caption("""
    **Allegro Price Monitor**  
    Wersja 1.3 · źródło: scrape.do
    
    Tryb konsolowy:
    ```
    python src/main.py run -i plik.csv
    ```
    """)


if __name__ == "__main__":
    main()
