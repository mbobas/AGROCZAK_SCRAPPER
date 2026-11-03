"""
Przelicza istniejący JSON wyników filtrami rynkowymi i zapisuje CSV.
python -m tests.export_selling_filters
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.results_io import (
    analyzer_summary_row,
    filter_products,
    flatten_offers,
    load_results_json,
)

DEFAULTS = dict(
    markup_min_pct=None,
    markup_max_pct=None,
    min_buyers=1,
    min_match_pct=90.0,
)

JSON_PATH = ROOT / "data" / "output" / "results_2026-10-20_2316_szukanie_po_kodzie.json"
OUT_DIR = ROOT / "data" / "output"


def main() -> int:
    path = JSON_PATH
    if not path.exists():
        print("brak", path)
        return 1
    products = load_results_json(path)
    filtered = filter_products(products, **DEFAULTS)
    summary = [analyzer_summary_row(p, **DEFAULTS) for p in filtered]
    flat = flatten_offers(filtered, **DEFAULTS)

    print(
        f"produkty {len(products)} -> po filtrach {len(filtered)}; "
        f"Wszytkie oferty {len(flat)}"
    )
    if summary:
        with_leader = sum(1 for r in summary if r.get("Kupujących max"))
        print(f"z liderem sprzedaży {with_leader}")

    sum_path = OUT_DIR / "verify_summary_selling.csv"
    off_path = OUT_DIR / "verify_offers_selling.csv"
    if summary:
        with sum_path.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(summary[0].keys()), delimiter=";")
            w.writeheader()
            w.writerows(summary)
    if flat:
        with off_path.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(flat[0].keys()), delimiter=";")
            w.writeheader()
            w.writerows(flat)
    print("zapisano", sum_path)
    print("zapisano", off_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
