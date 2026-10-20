"""
Cache wynikow - SQLite z TTL.
"""
import json
import sqlite3
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class CachedProduct:
    ean: str
    checked_at: str
    data: Dict[str, Any]

    def is_expired(self, ttl_days: int) -> bool:
        checked = datetime.fromisoformat(self.checked_at)
        return datetime.now() - checked > timedelta(days=ttl_days)


class ProductCache:
    """Cache wynikow w SQLite (thread-safe)."""

    def __init__(self, db_path: str = "data/cache.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self):
        with self._lock:
            with self._connect() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS products (
                        ean TEXT PRIMARY KEY,
                        checked_at TEXT NOT NULL,
                        data TEXT NOT NULL
                    )
                """)
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_checked_at ON products(checked_at)
                """)
                conn.commit()

    def get(self, ean: str) -> Optional[CachedProduct]:
        """Pobiera produkt z cache."""
        with self._lock:
            with self._connect() as conn:
                cursor = conn.execute(
                    "SELECT ean, checked_at, data FROM products WHERE ean = ?",
                    (ean,),
                )
                row = cursor.fetchone()
                if row:
                    return CachedProduct(
                        ean=row[0],
                        checked_at=row[1],
                        data=json.loads(row[2]),
                    )
        return None

    def set(self, ean: str, data: Dict[str, Any]):
        """Zapisuje produkt do cache."""
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO products (ean, checked_at, data)
                    VALUES (?, ?, ?)
                    """,
                    (ean, datetime.now().isoformat(), json.dumps(data, ensure_ascii=False)),
                )
                conn.commit()

    def get_if_valid(self, ean: str, ttl_days: int) -> Optional[Dict[str, Any]]:
        """Pobiera dane z cache jesli nie wygasly."""
        cached = self.get(ean)
        if cached and not cached.is_expired(ttl_days):
            return cached.data
        return None

    def get_many_if_valid(self, keys: List[str], ttl_days: int) -> Dict[str, Dict[str, Any]]:
        """
        Pobiera wiele wpisów z cache w jednym zapytaniu.
        Zwraca mapę key -> data tylko dla niewygasłych wpisów.
        """
        if not keys:
            return {}

        unique = list(dict.fromkeys(keys))
        found: Dict[str, Dict[str, Any]] = {}
        chunk_size = 400

        with self._lock:
            with self._connect() as conn:
                for i in range(0, len(unique), chunk_size):
                    chunk = unique[i : i + chunk_size]
                    placeholders = ",".join("?" * len(chunk))
                    cursor = conn.execute(
                        f"SELECT ean, checked_at, data FROM products WHERE ean IN ({placeholders})",
                        chunk,
                    )
                    for row in cursor.fetchall():
                        cached = CachedProduct(
                            ean=row[0],
                            checked_at=row[1],
                            data=json.loads(row[2]),
                        )
                        if not cached.is_expired(ttl_days):
                            found[cached.ean] = cached.data
        return found

    def get_all(self) -> List[CachedProduct]:
        """Pobiera wszystkie produkty z cache."""
        with self._lock:
            with self._connect() as conn:
                cursor = conn.execute("SELECT ean, checked_at, data FROM products")
                return [
                    CachedProduct(ean=row[0], checked_at=row[1], data=json.loads(row[2]))
                    for row in cursor.fetchall()
                ]

    def get_stats(self) -> Dict[str, Any]:
        """Zwraca statystyki cache."""
        with self._lock:
            with self._connect() as conn:
                total = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
                oldest = conn.execute("SELECT MIN(checked_at) FROM products").fetchone()[0]
                newest = conn.execute("SELECT MAX(checked_at) FROM products").fetchone()[0]

        return {
            "total_products": total,
            "oldest_check": oldest,
            "newest_check": newest,
        }

    def clear_expired(self, ttl_days: int) -> int:
        """Usuwa wygasle wpisy, zwraca liczbe usunietych."""
        cutoff = (datetime.now() - timedelta(days=ttl_days)).isoformat()
        with self._lock:
            with self._connect() as conn:
                cursor = conn.execute(
                    "DELETE FROM products WHERE checked_at < ?",
                    (cutoff,),
                )
                conn.commit()
                return cursor.rowcount

    def clear_all(self):
        """Czysci caly cache."""
        with self._lock:
            with self._connect() as conn:
                conn.execute("DELETE FROM products")
                conn.commit()
