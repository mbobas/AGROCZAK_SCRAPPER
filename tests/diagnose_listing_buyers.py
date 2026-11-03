"""
Próbka scrape.do: liczba kupujących vs surowe pola listingu.
Uruchom ręcznie (nie CI): python -m tests.diagnose_listing_buyers
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from src.api.scraper import (  # noqa: E402
    ScrapeDoClient,
    _extract_listing_store_state,
    parse_allegro_search_html,
)

OUT_DIR = ROOT / "data" / "logs" / "diagnose"
HTML_DIR = OUT_DIR / "html"

CODES = [
    "2654407",
    "JC334V6243",
    "MA109752",
    "CBS7513505",
    "4816636",
    "ES8T",
    "1432045071",
    "1432047071",
    "510515347",
    "SC8P",
    "ES8S",
    "1919000412",
    "MA299885",
    "B711W063400D",
    "CNV0821815M",
    "5140929941",
    "26900046546310C",
    "A950111210016",
    "B250110",
    "ECF838P",
]
RENDER_TRUE = ["2654407", "ES8T", "1432045071", "JC334V6243", "510515347"]

INTERESTING_KEY = re.compile(
    r"popular|sold|buy|kupi|sale|quantity|osob",
    re.IGNORECASE,
)


def _walk(obj: Any, path: str = "", out: Optional[List[tuple]] = None, depth: int = 0):
    if out is None:
        out = []
    if depth > 8:
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else str(k)
            if INTERESTING_KEY.search(str(k)):
                out.append((p, v if not isinstance(v, (dict, list)) else type(v).__name__))
            if isinstance(v, (dict, list)):
                _walk(v, p, out, depth + 1)
            elif INTERESTING_KEY.search(str(v)):
                out.append((p, v))
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:8]):
            _walk(v, f"{path}[{i}]", out, depth + 1)
    return out


def _top_item_keys(item: dict) -> List[str]:
    return sorted(item.keys())


def run_one(client: ScrapeDoClient, code: str, render: bool) -> Dict[str, Any]:
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    from urllib.parse import quote_plus

    search_url = f"https://allegro.pl/listing?string={quote_plus(code)}"
    html = client.scrape(search_url, render=render)
    tag = "render" if render else "norender"
    html_path = HTML_DIR / f"{code}_{tag}.html"
    html_path.write_text(html, encoding="utf-8")

    elements, meta = _extract_listing_store_state(html)
    parsed = parse_allegro_search_html(html)
    parsed_buyers = [o.buyers_count for o in parsed]
    with_buyers = sum(1 for b in parsed_buyers if b is not None)

    sample_fields: List[Dict[str, Any]] = []
    all_interesting: List[tuple] = []
    for item in elements[:8]:
        if not isinstance(item, dict):
            continue
        interesting = _walk(item)
        all_interesting.extend(interesting)
        sample_fields.append(
            {
                "keys": _top_item_keys(item),
                "productPopularity": item.get("productPopularity"),
                "popularity": item.get("popularity"),
                "interesting": interesting[:40],
            }
        )

    uniq_paths = sorted({p for p, _ in all_interesting})
    leader = None
    if parsed:
        sold = [o for o in parsed if o.buyers_count]
        leader = max(sold, key=lambda o: o.buyers_count or 0) if sold else None

    return {
        "code": code,
        "render": render,
        "html_bytes": len(html.encode("utf-8", errors="replace")),
        "html_path": str(html_path),
        "parse_meta": meta,
        "elements": len(elements),
        "offers_parsed": len(parsed),
        "offers_with_buyers": with_buyers,
        "buyers_values": parsed_buyers[:30],
        "leader_title": leader.title if leader else None,
        "leader_price": leader.price if leader else None,
        "leader_buyers": leader.buyers_count if leader else None,
        "interesting_paths": uniq_paths,
        "sample_items": sample_fields[:3],
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    client = ScrapeDoClient()
    info = client.get_credits_info()
    print("credits_info", {k: info.get(k) for k in info if k != "token"} if isinstance(info, dict) else info)

    rows: List[Dict[str, Any]] = []
    jobs = [(c, False) for c in CODES] + [(c, True) for c in RENDER_TRUE]
    for code, render in jobs:
        print(f"--- {code} render={render} ---")
        try:
            row = run_one(client, code, render)
        except Exception as exc:
            row = {"code": code, "render": render, "error": str(exc)}
        rows.append(row)
        print(
            json.dumps(
                {
                    "code": row.get("code"),
                    "render": row.get("render"),
                    "offers": row.get("offers_parsed"),
                    "with_buyers": row.get("offers_with_buyers"),
                    "leader_buyers": row.get("leader_buyers"),
                    "leader_price": row.get("leader_price"),
                    "interesting_paths": row.get("interesting_paths"),
                    "error": row.get("error"),
                    "remaining": client.stats.remaining_credits,
                    "session_cost": client.stats.total_credits_used,
                },
                ensure_ascii=False,
            )
        )

    out_path = OUT_DIR / "listing_buyers_sample.json"
    out_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print("saved", out_path)
    print("session_credits_used", client.stats.total_credits_used)
    print("remaining", client.stats.remaining_credits)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
