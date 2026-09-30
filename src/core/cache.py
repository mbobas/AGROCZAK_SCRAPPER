"""
Cache wynikow - SQLite z TTL.
"""
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict


@dataclass
class CachedProduct:
    ean: str
    checked_at: str
    data: Dict[str, Any]
    
    def is_expired(self, ttl_days: int) -> bool:
        checked = datetime.fromisoformat(self.checked_at)
        return datetime.now() - checked > timedelta(days=ttl_days)


class ProductCache:
    """Cache wynikow w SQLite."""
    
    def __init__(self, db_path: str = "data/cache.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
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
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT ean, checked_at, data FROM products WHERE ean = ?",
                (ean,)
            )
            row = cursor.fetchone()
            if row:
                return CachedProduct(
                    ean=row[0],
                    checked_at=row[1],
                    data=json.loads(row[2])
                )
        return None
    
    def set(self, ean: str, data: Dict[str, Any]):
        """Zapisuje produkt do cache."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO products (ean, checked_at, data)
                VALUES (?, ?, ?)
            """, (ean, datetime.now().isoformat(), json.dumps(data, ensure_ascii=False)))
            conn.commit()
    
    def get_if_valid(self, ean: str, ttl_days: int) -> Optional[Dict[str, Any]]:
        """Pobiera dane z cache jesli nie wygasly."""
        cached = self.get(ean)
        if cached and not cached.is_expired(ttl_days):
            return cached.data
        return None
    
    def get_all(self) -> List[CachedProduct]:
        """Pobiera wszystkie produkty z cache."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT ean, checked_at, data FROM products")
            return [
                CachedProduct(ean=row[0], checked_at=row[1], data=json.loads(row[2]))
                for row in cursor.fetchall()
            ]
    
    def get_stats(self) -> Dict[str, Any]:
        """Zwraca statystyki cache."""
        with sqlite3.connect(self.db_path) as conn:
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
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM products WHERE checked_at < ?",
                (cutoff,)
            )
            conn.commit()
            return cursor.rowcount
    
    def clear_all(self):
        """Czysci caly cache."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM products")
            conn.commit()
