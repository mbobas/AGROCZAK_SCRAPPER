"""
Świeży listing 30 kodów (bez cache) + do 20 stron ofert przy match 100%.
python -m tests.rescrape_sample_30
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from src.api.scraper import (  # noqa: E402
    ScrapeDoClient,
    offer_page_url,
    parse_allegro_offer_html,
    search_allegro_by_ean,
)
from src.core.cache import ProductCache
from src.core.matching import name_match_pct
from src.core.processor import InputProduct, ProductProcessor
from src.core.results_io import (
    analyzer_summary_row,
    load_results_json,
    offer_match_pct,
    save_results_json,
)

SAMPLE_BEFORE = ROOT / "data" / "output" / "results_sample_30_szukanie_po_kodzie.json"
AFTER_LISTING = ROOT / "data" / "output" / "sample_30_after_listing.json"
AFTER_OFFERS = ROOT / "data" / "output" / "sample_30_after_offers.json"
COMPARE_CSV = ROOT / "data" / "output" / "sample_30_compare.csv"
HTML_OFFERS = ROOT / "data" / "logs" / "diagnose" / "offers"
META = ROOT / "data" / "output" / "sample_30_meta.json"
MAX_OFFER_PAGES = 20


def _summary(p: dict) -> dict:
    return analyzer_summary_row(
        p,
        markup_min_pct=None,
        markup_max_pct=None,
        min_buyers=None,
        min_match_pct=0.0,
    )


def _leader_100(product: dict) -> Optional[dict]:
    scored: List[Tuple[int, float, dict]] = []
    for offer in product.get("offers") or []:
        pct = offer_match_pct(product, offer)
        if pct is None or pct < 100:
            continue
        buyers = offer.get("buyers_count")
        b = int(buyers) if buyers is not None else 0
        try:
            price = float(offer.get("price") or 0)
        except (TypeError, ValueError):
            price = 0.0
        oid = str(offer.get("offer_id") or "")
        scored.append((b, price if price else 10**9, oid, offer))
    if not scored:
        return None
    scored.sort(key=lambda t: (-t[0], t[1], t[2]))
    return scored[0][3]


def listing_scrape(products: List[dict]) -> Tuple[List[dict], ScrapeDoClient]:
    cache = ProductCache()
    keys = [str(p.get("ean")) for p in products]
    removed = cache.delete_keys(keys)
    print("usunieto z cache (tylko próbka)", removed)

    client = ScrapeDoClient()
    processor = ProductProcessor(search_mode="code")

    def fetch(query: str) -> list:
        offers = search_allegro_by_ean(query, client, render=False)
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

    processor.data_fetcher = fetch
    out: List[dict] = []
    for p in products:
        inp = InputProduct(
            ean=str(p.get("ean") or ""),
            my_price=float(p.get("my_price") or 0),
            name=p.get("name"),
        )
        result = processor.process_single(inp, skip_cache=True)
        d = result.to_dict()
        d["_sample_bucket"] = p.get("_sample_bucket")
        out.append(d)
        print(
            f"listing {inp.ean} offers={len(d.get('offers') or [])} "
            f"remaining={client.stats.remaining_credits} cost={client.stats.total_credits_used}"
        )
    save_results_json(out, AFTER_LISTING, search_mode="code")
    print("zapisano", AFTER_LISTING, "credits_used", client.stats.total_credits_used)
    return out, client


def pick_offer_targets(products: List[dict], cap: int = MAX_OFFER_PAGES) -> List[dict]:
    """Lider 100% na produkt, potem najtańsza 100%, max cap."""
    rows: List[dict] = []
    for p in products:
        leader = _leader_100(p)
        if not leader:
            continue
        url = offer_page_url(leader)
        if not url:
            continue
        rows.append(
            {
                "ean": p.get("ean"),
                "bucket": p.get("_sample_bucket"),
                "offer": leader,
                "url": url,
                "priority": 0 if (leader.get("buyers_count") or 0) else 1,
            }
        )
    rows.sort(key=lambda r: (r["priority"], r.get("ean") or ""))
    # unique offer_id
    seen = set()
    picked = []
    for r in rows:
        oid = str((r["offer"] or {}).get("offer_id") or r["url"])
        if oid in seen:
            continue
        seen.add(oid)
        picked.append(r)
        if len(picked) >= cap:
            break
    return picked


def scrape_offer_pages(client: ScrapeDoClient, products: List[dict], targets: List[dict]) -> List[dict]:
    HTML_OFFERS.mkdir(parents=True, exist_ok=True)
    by_ean = {str(p.get("ean")): p for p in products}
    details: List[dict] = []
    for t in targets:
        url = t["url"]
        ean = str(t["ean"])
        listing_offer = t["offer"]
        print(f"offer-page {ean} {url}")
        html = ""
        parsed = None
        err = None
        try:
            html = client.scrape(url, render=False)
            parsed = parse_allegro_offer_html(html)
        except Exception as exc:
            err = str(exc)
        html_path = HTML_OFFERS / f"{ean}_{listing_offer.get('offer_id')}.html"
        if html:
            html_path.write_text(html, encoding="utf-8")
        rec = {
            "ean": ean,
            "bucket": t.get("bucket"),
            "url": url,
            "buyers_listing": listing_offer.get("buyers_count"),
            "price_listing": listing_offer.get("price"),
            "title_listing": listing_offer.get("title"),
            "buyers_offer_page": parsed.buyers_count if parsed else None,
            "price_offer_page": parsed.price if parsed else None,
            "title_offer_page": parsed.title if parsed else None,
            "error": err,
            "html_path": str(html_path) if html else None,
            "html_bytes": len(html.encode("utf-8", errors="replace")) if html else 0,
        }
        details.append(rec)
        prod = by_ean.get(ean)
        if prod and parsed:
            for o in prod.get("offers") or []:
                if str(o.get("offer_id")) == str(listing_offer.get("offer_id")):
                    o["buyers_listing"] = o.get("buyers_count")
                    o["price_listing"] = o.get("price")
                    o["buyers_offer_page"] = parsed.buyers_count
                    o["price_offer_page"] = parsed.price
                    if parsed.buyers_count is not None:
                        o["buyers_count"] = parsed.buyers_count
                    if parsed.price:
                        o["price"] = parsed.price
                    break
        print(
            json.dumps(
                {
                    "ean": ean,
                    "buyers_listing": rec["buyers_listing"],
                    "buyers_offer": rec["buyers_offer_page"],
                    "price_listing": rec["price_listing"],
                    "price_offer": rec["price_offer_page"],
                    "remaining": client.stats.remaining_credits,
                },
                ensure_ascii=False,
            )
        )
    save_results_json(products, AFTER_OFFERS, search_mode="code")
    (HTML_OFFERS / "offer_page_compare.json").write_text(
        json.dumps(details, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return details


def write_compare(before: List[dict], after: List[dict], offer_details: List[dict]) -> None:
    after_map = {str(p.get("ean")): p for p in after}
    offer_map = {d["ean"]: d for d in offer_details}
    rows = []
    for p in before:
        ean = str(p.get("ean"))
        b = _summary(p)
        a = _summary(after_map.get(ean) or {"ean": ean, "offers": []})
        od = offer_map.get(ean) or {}
        rows.append(
            {
                "Kod": ean,
                "Bucket": p.get("_sample_bucket"),
                "Nazwa": p.get("name"),
                "Cena min stara": b.get("Cena min"),
                "Cena min nowa": a.get("Cena min"),
                "Kupujących max stara": b.get("Kupujących max"),
                "Kupujących max nowa listing": a.get("Kupujących max"),
                "Cena lidera stara": b.get("Cena lidera"),
                "Cena lidera nowa": a.get("Cena lidera"),
                "Tytuł lidera nowy": a.get("Tytuł lidera"),
                "buyers_listing": od.get("buyers_listing"),
                "buyers_offer_page": od.get("buyers_offer_page"),
                "price_listing": od.get("price_listing"),
                "price_offer_page": od.get("price_offer_page"),
                "url_oferty": od.get("url"),
                "Liczba ofert stara": b.get("Liczba ofert"),
                "Liczba ofert nowa": a.get("Liczba ofert"),
            }
        )
    with COMPARE_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(rows)
    print("zapisano", COMPARE_CSV)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--offers-only",
        action="store_true",
        help="Pomiń listing; wczytaj sample_30_after_listing.json",
    )
    args = parser.parse_args()
    before = load_results_json(SAMPLE_BEFORE)
    buckets = {p.get("ean"): p.get("_sample_bucket") for p in before}
    if args.offers_only and AFTER_LISTING.exists():
        after = load_results_json(AFTER_LISTING)
        for p in after:
            p["_sample_bucket"] = buckets.get(p.get("ean")) or p.get("_sample_bucket")
        client = ScrapeDoClient()
        print("offers-only, listing z", AFTER_LISTING)
    else:
        print("start listing n=", len(before))
        after, client = listing_scrape(before)
        for p in after:
            p["_sample_bucket"] = buckets.get(p.get("ean"))
    targets = pick_offer_targets(after)
    print("offer targets", len(targets), [t["ean"] for t in targets])
    details = scrape_offer_pages(client, after, targets)
    write_compare(before, after, details)
    print("session_credits_used", client.stats.total_credits_used)
    print("remaining", client.stats.remaining_credits)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
