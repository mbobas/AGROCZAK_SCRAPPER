"""
Buduje próbkę 30 kodów z plików złych outputów + JSON 16k.
python -m tests.build_sample_30
"""
from __future__ import annotations

import csv
import json
import random
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.results_io import load_results_json, offer_match_pct, offer_match_reason

CSV_OFFERS = ROOT / "data" / "przyklady_zly_outputow" / "oferty_200k.csv"
JSON_16K = ROOT / "data" / "output" / "results_2026-10-20_2316_szukanie_po_kodzie.json"
CACHE = ROOT / "data" / "cache.db"
OUT_JSON = ROOT / "data" / "output" / "results_sample_30_szukanie_po_kodzie.json"
OUT_META = ROOT / "data" / "output" / "sample_30_meta.json"
SEED = 20261030


def _num(val: str) -> bool:
    s = (val or "").strip()
    if not s:
        return False
    try:
        float(s.replace(",", "."))
        return True
    except ValueError:
        return False


def _load_csv_groups() -> Dict[str, List[dict]]:
    by: Dict[str, List[dict]] = defaultdict(list)
    with CSV_OFFERS.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            by[row["Kod"]].append(row)
    return by


def pick_codes(by: Dict[str, List[dict]]) -> Dict[str, List[str]]:
    worst: List[Tuple[int, str]] = []
    sold: List[Tuple[int, str]] = []
    for kod, rows in by.items():
        m100 = []
        for row in rows:
            try:
                m = float((row.get("Dopasowanie %") or "0").replace(",", "."))
            except ValueError:
                continue
            if m >= 100:
                m100.append(row)
        if not m100:
            continue
        empty_buy = sum(1 for r in m100 if not (r.get("Kupujących") or "").strip())
        has_buy = sum(1 for r in m100 if _num(r.get("Kupujących") or ""))
        empty_price = sum(1 for r in m100 if not (r.get("Cena") or "").strip())
        bad_price = sum(
            1
            for r in m100
            if (r.get("Cena") or "").strip() and not _num(r.get("Cena") or "")
        )
        if bad_price or empty_price or empty_buy == len(m100):
            score = 1000 * bad_price + 100 * empty_price + empty_buy
            worst.append((score, kod))
        if has_buy:
            sold.append((has_buy, kod))
    worst.sort(reverse=True)
    sold.sort(reverse=True)
    worst10 = [k for _, k in worst[:10]]
    sold10: List[str] = []
    used = set(worst10)
    for _, k in sold:
        if k in used:
            continue
        sold10.append(k)
        used.add(k)
        if len(sold10) >= 10:
            break
    rng = random.Random(SEED)
    rest = [k for k in by.keys() if k not in used]
    rng.shuffle(rest)
    random10 = rest[:10]
    return {"worst": worst10, "sold": sold10, "random": random10}


def main() -> int:
    if CACHE.exists():
        bak = ROOT / "data" / f"cache.db.bak_{datetime.now().strftime('%Y%m%d_%H%M')}"
        shutil.copy2(CACHE, bak)
        print("cache backup", bak)
    else:
        print("brak cache.db — pomijam kopię")

    by = _load_csv_groups()
    groups = pick_codes(by)
    ordered = groups["worst"] + groups["sold"] + groups["random"]
    print("worst", groups["worst"])
    print("sold", groups["sold"])
    print("random", groups["random"])

    products_all = load_results_json(JSON_16K)
    by_ean = {str(p.get("ean")): p for p in products_all}
    picked: List[Dict[str, Any]] = []
    missing = []
    bucket_of = {}
    for i, kod in enumerate(ordered):
        bucket = "worst" if i < 10 else "sold" if i < 20 else "random"
        bucket_of[kod] = bucket
        p = by_ean.get(kod)
        if not p:
            missing.append(kod)
            continue
        clone = dict(p)
        clone["_sample_bucket"] = bucket
        picked.append(clone)

    payload = {
        "generated_at": datetime.now().isoformat(),
        "sample": True,
        "products": picked,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    meta = {
        "groups": groups,
        "missing_in_json": missing,
        "count": len(picked),
        "json": str(OUT_JSON),
        "note": "Wczytaj w Analizie: results_sample_30_szukanie_po_kodzie.json",
    }
    OUT_META.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print("zapisano", OUT_JSON, "n=", len(picked), "brak w JSON", missing)
    # sanity: 100% match empty buyers in worst
    for kod in groups["worst"][:3]:
        p = by_ean.get(kod) or {}
        offers = p.get("offers") or []
        n100 = 0
        n100_buy = 0
        for o in offers:
            pct = offer_match_pct(p, o)
            if pct is not None and pct >= 100:
                n100 += 1
                if o.get("buyers_count"):
                    n100_buy += 1
        print("check", kod, "offers", len(offers), "m100", n100, "m100_with_buyers", n100_buy)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
