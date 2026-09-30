"""
Logger zapytań HTTP / scrapowania — pliki JSON (+ HTML gdy 0 ofert).
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

LOG_ROOT = Path("data/logs")
REQUESTS_DIR = LOG_ROOT / "requests"
HTML_DIR = LOG_ROOT / "html"

_LAST_LOG: Optional[Dict[str, Any]] = None


def get_last_log() -> Optional[Dict[str, Any]]:
    """Ostatni zapisany skrót logu (dla GUI)."""
    return _LAST_LOG


def logs_dir() -> Path:
    REQUESTS_DIR.mkdir(parents=True, exist_ok=True)
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_ROOT


def _safe_code(code: Optional[str]) -> str:
    if not code:
        return "unknown"
    return re.sub(r"[^\w\-]+", "_", str(code))[:80]


def log_request(
    *,
    source: str,
    url: str,
    code: Optional[str] = None,
    http_status: Optional[int] = None,
    error: Optional[str] = None,
    response_text: Optional[str] = None,
    offers_parsed: int = 0,
    offer_titles: Optional[List[str]] = None,
    extra: Optional[Dict[str, Any]] = None,
    save_html_on_empty: bool = True,
) -> Path:
    """
    Zapisuje log jednego zapytania do data/logs/requests/.
    Przy offers_parsed == 0 i niepustym response_text zapisuje też HTML.
    """
    global _LAST_LOG
    logs_dir()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe = _safe_code(code)
    preview = ""
    html_bytes = 0
    html_path = None

    if response_text is not None:
        html_bytes = len(response_text.encode("utf-8", errors="replace"))
        preview = response_text[:4000]
        if save_html_on_empty and offers_parsed == 0 and response_text:
            html_file = HTML_DIR / f"{safe}_{ts}.html"
            html_file.write_text(response_text, encoding="utf-8")
            html_path = str(html_file)

    titles = (offer_titles or [])[:10]
    payload: Dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "code": code,
        "url": url,
        "http_status": http_status,
        "error": error,
        "html_bytes": html_bytes,
        "response_preview": preview,
        "offers_parsed": offers_parsed,
        "offer_titles": titles,
        "html_path": html_path,
    }
    if extra:
        payload["extra"] = extra

    out_path = REQUESTS_DIR / f"{safe}_{ts}.json"
    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    _LAST_LOG = {
        "path": str(out_path),
        "source": source,
        "code": code,
        "offers_parsed": offers_parsed,
        "error": error,
        "http_status": http_status,
        "html_path": html_path,
    }
    return out_path
