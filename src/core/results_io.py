"""
Zapis / odczyt wyników scrapowania (JSON w data/output/).
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .matching import code_in_title, name_match_pct

OUTPUT_DIR = Path("data/output")


def ensure_output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def search_mode_suffix(mode: Optional[str]) -> str:
    """Suffix nazwy pliku: _szukanie_po_kodzie | _szukanie_po_nazwie."""
    if str(mode or "").strip().lower() in {"name", "nazwa"}:
        return "_szukanie_po_nazwie"
    return "_szukanie_po_kodzie"


def infer_search_mode(results: List[Any]) -> str:
    """Tryb z pierwszego produktu z polem search_mode; domyślnie code."""
    for item in results or []:
        if isinstance(item, dict):
            mode = item.get("search_mode")
        else:
            mode = getattr(item, "search_mode", None)
        if mode in ("code", "name"):
            return str(mode)
    return "code"


def dedupe_offers(offers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deduplikuje oferty po offer_id (puste id zostawia unikalne po kolejności)."""
    seen: set[str] = set()
    out: List[Dict[str, Any]] = []
    for i, offer in enumerate(offers or []):
        oid = str(offer.get("offer_id") or "").strip()
        key = oid if oid else f"__anon_{i}"
        if key in seen:
            continue
        seen.add(key)
        out.append(offer)
    return out


def offer_match_pct(product: Dict[str, Any], offer: Dict[str, Any]) -> Optional[float]:
    """Dopasowanie nazwy produktu do tytulu oferty (None gdy brak nazwy)."""
    return name_match_pct(product.get("name"), offer.get("title"), product.get("ean"))


def offer_match_reason(product: Dict[str, Any], offer: Dict[str, Any]) -> str:
    """Skad dopasowanie: kod (kod w tytule), slowa (z nazwy) lub pusty."""
    if code_in_title(product.get("ean"), offer.get("title")):
        pct = offer_match_pct(product, offer)
        return "kod+nazwa" if pct is not None and pct >= 100 else "tylko kod"
    return "slowa" if product.get("name") else ""


def _mode_label(product: Dict[str, Any]) -> str:
    return "Nazwa" if product.get("search_mode") == "name" else "Kod"


def _match_ok(product: Dict[str, Any], offer: Dict[str, Any], min_match_pct: float) -> bool:
    if min_match_pct <= 0:
        return True
    pct = offer_match_pct(product, offer)
    return pct is not None and pct >= min_match_pct


def count_matching_offers(
    product: Dict[str, Any],
    *,
    min_markup: float = 0.0,
    max_markup: float = 0.50,
    min_buyers: int = 0,
    min_match_pct: float = 0.0,
) -> List[Dict[str, Any]]:
    """
    Oferty pasujące do bieżących filtrów (marża + kupujący).
    min_buyers <= 0: nie wymagaj buyers_count (null OK).
    """
    offers = dedupe_offers(product.get("offers") or [])
    my_price = float(product.get("my_price") or 0)
    if my_price <= 0:
        return []

    matched: List[Dict[str, Any]] = []
    for offer in offers:
        try:
            price = float(offer.get("price") or 0)
        except (TypeError, ValueError):
            continue
        if price <= 0:
            continue
        lo = my_price * (1 + min_markup)
        hi = my_price * (1 + max_markup)
        if not (lo <= price <= hi):
            continue
        if min_buyers > 0:
            buyers = offer.get("buyers_count")
            if buyers is None or int(buyers) < min_buyers:
                continue
        if not _match_ok(product, offer, min_match_pct):
            continue
        matched.append(offer)
    return matched


def offer_stats(
    product: Dict[str, Any],
    *,
    min_markup: Optional[float] = None,
    max_markup: Optional[float] = None,
    min_buyers: Optional[int] = None,
    min_match_pct: float = 0.0,
) -> Dict[str, Any]:
    """Statystyki ofert produktu (po dedupie). Pasujące wg podanych filtrów lub zapisanych matching_offers."""
    offers = dedupe_offers(product.get("offers") or [])
    my_price = float(product.get("my_price") or 0)
    prices = []
    for o in offers:
        try:
            p = float(o.get("price") or 0)
            if p > 0:
                prices.append(p)
        except (TypeError, ValueError):
            continue

    cheapest = None
    if offers and prices:
        cheapest = min(
            (o for o in offers if float(o.get("price") or 0) > 0),
            key=lambda o: float(o.get("price") or 0),
            default=None,
        )

    min_price = min(prices) if prices else None
    max_price = max(prices) if prices else None
    markup_min = None
    if min_price is not None and my_price > 0:
        markup_min = round((min_price / my_price - 1) * 100, 1)

    if min_markup is not None and max_markup is not None and min_buyers is not None:
        matching = count_matching_offers(
            product,
            min_markup=min_markup,
            max_markup=max_markup,
            min_buyers=min_buyers,
            min_match_pct=min_match_pct,
        )
    else:
        matching = product.get("matching_offers") or []

    match_values = [
        m for m in (offer_match_pct(product, o) for o in offers) if m is not None
    ]
    best_match_pct = max(match_values) if match_values else None

    return {
        "offers_count": len(offers),
        "offers": offers,
        "min_price": min_price,
        "max_price": max_price,
        "cheapest_title": (cheapest or {}).get("title") if cheapest else None,
        "cheapest_price": float(cheapest["price"]) if cheapest else None,
        "markup_min_pct": markup_min,
        "matching_count": len(matching),
        "matching_offers": matching,
        "best_match_pct": best_match_pct,
    }


def format_status(status: Optional[str]) -> str:
    """Status z ikoną do wyświetlenia w tabeli."""
    labels = {
        "checked": "✅ checked",
        "error": "❌ error",
        "pending": "⏳ pending",
    }
    if not status:
        return ""
    return labels.get(str(status), str(status))


def summary_row(
    product: Dict[str, Any],
    *,
    min_markup: Optional[float] = None,
    max_markup: Optional[float] = None,
    min_buyers: Optional[int] = None,
    min_match_pct: float = 0.0,
) -> Dict[str, Any]:
    """Jeden wiersz tabeli podsumowania. Filtry opcjonalne — do żywego „Pasujące”."""
    stats = offer_stats(
        product,
        min_markup=min_markup,
        max_markup=max_markup,
        min_buyers=min_buyers,
        min_match_pct=min_match_pct,
    )
    return {
        "Kod": product.get("ean"),
        "Nazwa": product.get("name"),
        "Tryb": _mode_label(product),
        "Moja cena": product.get("my_price"),
        "Znaleziono": "✅ tak" if product.get("found_on_allegro") else "❌ nie",
        "Liczba ofert": stats["offers_count"],
        "Cena min": stats["min_price"],
        "Cena max": stats["max_price"],
        "Najtańsza oferta": stats["cheapest_title"],
        "Marża min %": stats["markup_min_pct"],
        "Dopasowanie max %": stats["best_match_pct"],
        "Pasujące": stats["matching_count"],
        "Status": format_status(product.get("status")),
        "Cache": "tak" if product.get("from_cache") else "",
        "Błąd": product.get("error_message") or "",
    }



def filter_offers(
    product: Dict[str, Any],
    *,
    markup_min_pct: Optional[float] = None,
    markup_max_pct: Optional[float] = None,
    min_buyers: Optional[int] = None,
    min_match_pct: float = 0.0,
) -> List[Dict[str, Any]]:
    """
    Oferty produktu (po dedupie) spełniające filtry — jedno źródło prawdy.
    markup_*_pct None = brak ograniczenia (nieskończoność); bez żadnej granicy
    przechodzą też oferty bez ceny/mojej ceny.
    min_buyers None/0 = bez filtra (None w buyers_count przechodzi);
    >= 1 = oferta musi mieć buyers_count >= min_buyers.
    """
    my_price = float(product.get("my_price") or 0)
    check_markup = markup_min_pct is not None or markup_max_pct is not None
    out: List[Dict[str, Any]] = []
    for offer in dedupe_offers(product.get("offers") or []):
        try:
            price = float(offer.get("price") or 0)
        except (TypeError, ValueError):
            price = 0.0
        if check_markup:
            if price <= 0 or my_price <= 0:
                continue
            markup = round((price / my_price - 1) * 100, 6)  # szum float
            if markup_min_pct is not None and markup < markup_min_pct:
                continue
            if markup_max_pct is not None and markup > markup_max_pct:
                continue
        if min_buyers is not None and min_buyers > 0:
            buyers = offer.get("buyers_count")
            if buyers is None or int(buyers) < min_buyers:
                continue
        if not _match_ok(product, offer, min_match_pct):
            continue
        out.append(offer)
    return out


def analyzer_summary_row(
    product: Dict[str, Any],
    *,
    markup_min_pct: Optional[float] = None,
    markup_max_pct: Optional[float] = None,
    min_buyers: Optional[int] = None,
    min_match_pct: float = 0.0,
) -> Dict[str, Any]:
    """Wiersz podsumowania liczony wyłącznie z przefiltrowanych ofert."""
    offers = filter_offers(
        product,
        markup_min_pct=markup_min_pct,
        markup_max_pct=markup_max_pct,
        min_buyers=min_buyers,
        min_match_pct=min_match_pct,
    )
    clone = dict(product)
    clone["offers"] = offers
    clone["matching_offers"] = offers
    return summary_row(clone)


def flatten_offers(
    products: List[Dict[str, Any]],
    *,
    min_match_pct: float = 0.0,
    markup_min_pct: Optional[float] = None,
    markup_max_pct: Optional[float] = None,
    min_buyers: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Spłaszcza produkty × oferty (po dedupie) — tylko oferty spełniające filtry."""
    rows: List[Dict[str, Any]] = []
    for product in products:
        my_price = float(product.get("my_price") or 0)
        product_offers = filter_offers(
            product,
            markup_min_pct=markup_min_pct,
            markup_max_pct=markup_max_pct,
            min_buyers=min_buyers,
            min_match_pct=min_match_pct,
        )
        product_offers.sort(
            key=lambda o: -(offer_match_pct(product, o) or 0.0)
        )
        for offer in product_offers:
            try:
                price = float(offer.get("price") or 0)
            except (TypeError, ValueError):
                price = 0.0
            markup = None
            if price > 0 and my_price > 0:
                markup = round((price / my_price - 1) * 100, 1)
            rows.append(
                {
                    "Kod": product.get("ean"),
                    "Nazwa": product.get("name"),
                    "Tryb": _mode_label(product),
                    "Moja cena": my_price,
                    "Dopasowanie %": offer_match_pct(product, offer),
                    "Powód": offer_match_reason(product, offer),
                    "Tytuł": offer.get("title"),
                    "Cena": price or None,
                    "Marża %": markup,
                    "Sprzedawca": offer.get("seller_name"),
                    "Kupujących": offer.get("buyers_count"),
                    "URL": offer.get("url"),
                    "offer_id": offer.get("offer_id"),
                }
            )
    return rows


def save_results_json(
    results: List[Dict[str, Any]],
    path: Optional[Path] = None,
    *,
    search_mode: Optional[str] = None,
) -> Path:
    """Zapisuje wyniki do pliku timestampowanego z suffixem trybu szukania."""
    ensure_output_dir()
    if path is None:
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        mode = search_mode if search_mode is not None else infer_search_mode(results)
        suffix = search_mode_suffix(mode)
        path = OUTPUT_DIR / f"results_{stamp}{suffix}.json"
    else:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_at": datetime.now().isoformat(),
        "products": results,
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def autosave_results(
    results: List[Dict[str, Any]],
    *,
    search_mode: Optional[str] = None,
) -> Path:
    """Zapis timestampowanego JSON z suffixem trybu szukania."""
    return save_results_json(results, search_mode=search_mode)


def list_result_files() -> List[Path]:
    """Lista plików results_*.json w data/output (najnowsze pierwsze)."""
    ensure_output_dir()
    files = list(OUTPUT_DIR.glob("results_*.json"))
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def load_results_json(path: Path) -> List[Dict[str, Any]]:
    """Wczytuje listę produktów z pliku wyników."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return list(data.get("products") or [])
    if isinstance(data, list):
        return data
    return []


def filter_products(
    products: List[Dict[str, Any]],
    *,
    markup_min_pct: Optional[float] = 0.0,
    markup_max_pct: Optional[float] = 50.0,
    min_offers: int = 0,
    require_offers: bool = True,
    min_buyers: Optional[int] = None,
    min_match_pct: float = 0.0,
) -> List[Dict[str, Any]]:
    """
    Lokalne filtrowanie produktów po ofertach spełniających filtry (filter_offers).
    Produkt zostaje, gdy liczba przefiltrowanych ofert >= max(min_offers, 1 gdy require_offers).
    markup_*_pct None = brak granicy (nieskończoność).
    """
    needed = max(int(min_offers), 1 if require_offers else 0)
    filtered: List[Dict[str, Any]] = []
    for product in products:
        offers = filter_offers(
            product,
            markup_min_pct=markup_min_pct,
            markup_max_pct=markup_max_pct,
            min_buyers=min_buyers,
            min_match_pct=min_match_pct,
        )
        if len(offers) >= needed:
            filtered.append(product)
    return filtered
