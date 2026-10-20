"""
Zapis / odczyt wyników scrapowania (JSON w data/output/).
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .matching import name_match_pct

OUTPUT_DIR = Path("data/output")
LATEST_NAME = "results_latest.json"


def ensure_output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


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
    return name_match_pct(product.get("name"), offer.get("title"))


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



def flatten_offers(
    products: List[Dict[str, Any]], *, min_match_pct: float = 0.0
) -> List[Dict[str, Any]]:
    """Spłaszcza produkty × oferty (po dedupie); oferty poniżej progu dopasowania pomijane."""
    rows: List[Dict[str, Any]] = []
    for product in products:
        my_price = float(product.get("my_price") or 0)
        product_offers = [
            o
            for o in dedupe_offers(product.get("offers") or [])
            if _match_ok(product, o, min_match_pct)
        ]
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
                    "Moja cena": my_price,
                    "Dopasowanie %": offer_match_pct(product, offer),
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
) -> Path:
    """Zapisuje wyniki do pliku timestampowanego (domyślnie)."""
    ensure_output_dir()
    if path is None:
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        path = OUTPUT_DIR / f"results_{stamp}.json"
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


def save_results_latest(results: List[Dict[str, Any]]) -> Path:
    """Nadpisuje results_latest.json."""
    return save_results_json(results, path=OUTPUT_DIR / LATEST_NAME)


def autosave_results(results: List[Dict[str, Any]]) -> Tuple[Path, Path]:
    """Zapis timestamp + latest. Zwraca (timestamp_path, latest_path)."""
    stamped = save_results_json(results)
    latest = save_results_latest(results)
    return stamped, latest


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
    markup_min_pct: float = 0.0,
    markup_max_pct: float = 50.0,
    min_offers: int = 0,
    require_offers: bool = True,
    min_buyers: Optional[int] = None,
    require_buyers: bool = False,
    match_mode: str = "any_in_range",
    min_match_pct: float = 0.0,
) -> List[Dict[str, Any]]:
    """
    Lokalne filtrowanie produktów.
    match_mode:
      - any_in_range: którakolwiek oferta w zakresie marży
      - cheapest_in_range: najtańsza oferta w zakresie marży
    """
    filtered: List[Dict[str, Any]] = []
    for product in products:
        stats = offer_stats(product)
        offers = stats["offers"]

        if require_offers and stats["offers_count"] == 0:
            continue
        if stats["offers_count"] < min_offers:
            continue

        my_price = float(product.get("my_price") or 0)

        def offer_ok(offer: Dict[str, Any]) -> bool:
            try:
                price = float(offer.get("price") or 0)
            except (TypeError, ValueError):
                return False
            if price <= 0 or my_price <= 0:
                return False
            markup = (price / my_price - 1) * 100
            if markup < markup_min_pct or markup > markup_max_pct:
                return False
            if not _match_ok(product, offer, min_match_pct):
                return False
            if require_buyers:
                buyers = offer.get("buyers_count")
                if buyers is None:
                    return False
                if min_buyers is not None and int(buyers) < min_buyers:
                    return False
            elif min_buyers is not None and min_buyers > 0:
                buyers = offer.get("buyers_count")
                if buyers is not None and int(buyers) < min_buyers:
                    return False
            return True

        if not offers:
            if not require_offers:
                filtered.append(product)
            continue

        if match_mode == "cheapest_in_range":
            priced = [o for o in offers if float(o.get("price") or 0) > 0]
            if not priced:
                continue
            cheapest = min(priced, key=lambda o: float(o.get("price") or 0))
            if offer_ok(cheapest):
                filtered.append(product)
        else:
            if any(offer_ok(o) for o in offers):
                filtered.append(product)

    return filtered
