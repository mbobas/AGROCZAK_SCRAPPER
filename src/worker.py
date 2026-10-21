"""
Worker joba scrapowania — osobny proces, niezależny od Streamlit.

Uruchomienie (robi to dashboard):
    python -m src.worker data/job_input.json

Postęp, pauza i stop idą przez data/job_status.json, więc UI może się
rozłączyć / odświeżyć i nadal widzi job.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import traceback
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

JOB_INPUT_PATH = Path("data/job_input.json")
WORKER_LOG_PATH = Path("data/worker.log")


def write_job_input(
    products: List[Any],
    *,
    search_mode: str,
    config: Any,
    workers: int,
    render: bool,
    path: Path = JOB_INPUT_PATH,
) -> Path:
    """Zapisuje parametry joba dla workera."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "search_mode": search_mode,
        "workers": int(workers),
        "render": bool(render),
        "config": asdict(config),
        "products": [
            {"ean": p.ean, "my_price": p.my_price, "name": p.name} for p in products
        ],
    }
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)
    return path


def spawn_worker(input_path: Path = JOB_INPUT_PATH) -> subprocess.Popen:
    """Startuje worker jako odłączony proces (przeżywa restart/crash Streamlit)."""
    WORKER_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log = open(WORKER_LOG_PATH, "a", encoding="utf-8")
    kwargs: Dict[str, Any] = {}
    if os.name == "nt":
        kwargs["creationflags"] = (
            subprocess.DETACHED_PROCESS
            | subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.CREATE_NO_WINDOW
        )
    else:
        kwargs["start_new_session"] = True
    return subprocess.Popen(
        [sys.executable, "-m", "src.worker", str(input_path)],
        cwd=str(ROOT),
        stdin=subprocess.DEVNULL,
        stdout=log,
        stderr=log,
        close_fds=True,
        **kwargs,
    )


def run(input_path: Path) -> int:
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
    os.chdir(ROOT)  # ścieżki data/... są względne

    from src.api.scraper import ScrapeDoClient, search_allegro_by_ean
    from src.core.job_state import write_status
    from src.core.processor import (
        InputProduct,
        ProcessorConfig,
        ProductProcessor,
    )

    try:
        payload = json.loads(Path(input_path).read_text(encoding="utf-8"))
        products = [InputProduct(**p) for p in payload["products"]]
        config = ProcessorConfig(**payload.get("config", {}))
        render = bool(payload.get("render", False))
        client = ScrapeDoClient()

        def fetch(query: str) -> list[dict]:
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

        processor = ProductProcessor(
            config=config,
            data_fetcher=fetch,
            search_mode=payload.get("search_mode", "code"),
        )
        processor.process_batch(
            products, max_workers=int(payload.get("workers", 1))
        )
        return 0
    except Exception as exc:  # processor sam zapisuje błąd w trakcie batcha
        traceback.print_exc()
        write_status(
            running=False,
            paused=False,
            phase="done",
            error=f"Worker: {exc}",
        )
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python -m src.worker <job_input.json>")
        sys.exit(2)
    sys.exit(run(Path(sys.argv[1])))
