"""
Stan bieżącego joba scrapowania — plik na dysku (widoczny po refresh UI).
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

STATUS_PATH = Path("data/job_status.json")
_LOCK = threading.Lock()

_DEFAULT: Dict[str, Any] = {
    "running": False,
    "paused": False,
    "stop_requested": False,
    "pause_requested": False,
    "progress": 0,
    "total": 0,
    "cache_hits": 0,
    "scraped": 0,
    "current_ean": None,
    "search_mode": "code",
    "partial_path": None,
    "final_path": None,
    "phase": None,  # cache_lookup | cache_apply | scrape | done
    "started_at": None,
    "updated_at": None,
    "error": None,
    "pid": None,
}


def _ensure_parent() -> None:
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)


def read_status() -> Dict[str, Any]:
    """Odczytuje status; przy braku/błędzie zwraca domyślny (running=False)."""
    with _LOCK:
        if not STATUS_PATH.exists():
            return dict(_DEFAULT)
        try:
            data = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return dict(_DEFAULT)
            out = dict(_DEFAULT)
            out.update(data)
            return out
        except (OSError, json.JSONDecodeError):
            return dict(_DEFAULT)


def write_status(**fields: Any) -> Dict[str, Any]:
    """
    Aktualizuje status (merge z istniejącym) i zapisuje atomowo.
    Zwraca zapisany słownik.
    """
    with _LOCK:
        current = dict(_DEFAULT)
        if STATUS_PATH.exists():
            try:
                raw = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    current.update(raw)
            except (OSError, json.JSONDecodeError):
                pass

        current.update(fields)
        current["updated_at"] = datetime.now().isoformat()

        _ensure_parent()
        tmp = STATUS_PATH.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps(current, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.replace(tmp, STATUS_PATH)
        return current


def request_stop() -> Dict[str, Any]:
    """Ustawia stop_requested=True (UI → wątek)."""
    return write_status(stop_requested=True)


def is_stop_requested() -> bool:
    return bool(read_status().get("stop_requested"))


def clear_status() -> None:
    """Czyści status po zakończeniu joba."""
    write_status(**dict(_DEFAULT))


def pid_alive(pid: Any) -> bool:
    """
    Czy proces o danym PID żyje — bez ubijania go.
    UWAGA: na Windows os.kill(pid, 0) wywołuje TerminateProcess i ZABIJA proces!
    """
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return False
    if pid <= 0:
        return False
    if os.name == "nt":
        import ctypes

        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        STILL_ACTIVE = 259
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            return False
        try:
            code = ctypes.c_ulong()
            if not kernel32.GetExitCodeProcess(handle, ctypes.byref(code)):
                return False
            return code.value == STILL_ACTIVE
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except PermissionError:
        return True
    except OSError:
        return False


def request_pause(paused: bool) -> Dict[str, Any]:
    """Ustawia pause_requested (UI -> worker)."""
    return write_status(pause_requested=bool(paused))


def is_pause_requested() -> bool:
    return bool(read_status().get("pause_requested"))


def is_stale_running(status: Optional[Dict[str, Any]] = None) -> bool:
    """True gdy status mówi running, ale proces joba (worker) już nie żyje."""
    st = status if status is not None else read_status()
    if not st.get("running"):
        return False
    return not pid_alive(st.get("pid"))
