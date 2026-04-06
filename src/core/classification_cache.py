"""
Кеш для результатів класифікації файлів через LLM
Зберігає результати в SQLite для уникнення повторних API викликів
"""

import sqlite3
import json
import time
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class ClassificationCache:
    """Кеш для результатів LLM класифікації"""

    def __init__(self, db_path: str = "classification_cache.db"):
        """
        Ініціалізувати кеш

        Args:
            db_path: Шлях до SQLite бази даних
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Створити таблицю кешу якщо не існує"""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS classification_cache (
                    filename TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    file_mtime INTEGER NOT NULL,
                    provider TEXT NOT NULL,
                    category TEXT NOT NULL,
                    subcategory TEXT,
                    description_uk TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    cached_at REAL NOT NULL,
                    PRIMARY KEY (filename, file_size, file_mtime)
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def get(self, filename: str, size: int, mtime: int) -> Optional[Dict[str, Any]]:
        """
        Отримати закешований результат

        Args:
            filename: Ім'я файлу
            size: Розмір файлу в байтах
            mtime: Час модифікації (timestamp)

        Returns:
            Dict з результатом класифікації або None якщо не знайдено
        """
        conn = sqlite3.connect(self.db_path)
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT provider, category, subcategory, description_uk,
                       confidence, cached_at
                FROM classification_cache
                WHERE filename = ? AND file_size = ? AND file_mtime = ?
            """, (filename, size, mtime))

            row = cursor.fetchone()

            if row is None:
                return None

            result = {
                "provider": row["provider"],
                "category": row["category"],
                "description_uk": row["description_uk"],
                "confidence": row["confidence"],
                "cached_at": row["cached_at"]
            }

            if row["subcategory"]:
                result["subcategory"] = row["subcategory"]

            return result
        finally:
            conn.close()

    def set(self, filename: str, size: int, mtime: int,
            provider: str, result: Dict[str, Any]):
        """
        Зберегти результат класифікації в кеш

        Args:
            filename: Ім'я файлу
            size: Розмір файлу в байтах
            mtime: Час модифікації (timestamp)
            provider: Ім'я LLM провайдера
            result: Результат класифікації (category, description_uk, confidence)
        """
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                INSERT OR REPLACE INTO classification_cache
                (filename, file_size, file_mtime, provider, category,
                 subcategory, description_uk, confidence, cached_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                filename,
                size,
                mtime,
                provider,
                result["category"],
                result.get("subcategory"),
                result.get("description_uk", ""),
                result.get("confidence", 0.0),
                time.time()
            ))
            conn.commit()
        finally:
            conn.close()

    def clear(self):
        """Очистити весь кеш"""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("DELETE FROM classification_cache")
            conn.commit()
        finally:
            conn.close()

    def get_stats(self) -> Dict[str, Any]:
        """
        Отримати статистику кешу

        Returns:
            Dict з статистикою: total_entries, by_provider
        """
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()

            # Загальна кількість записів
            cursor.execute("SELECT COUNT(*) FROM classification_cache")
            total = cursor.fetchone()[0]

            # Кількість по провайдерах
            cursor.execute("""
                SELECT provider, COUNT(*) as count
                FROM classification_cache
                GROUP BY provider
            """)

            by_provider = {row[0]: row[1] for row in cursor.fetchall()}

            return {
                "total_entries": total,
                "by_provider": by_provider
            }
        finally:
            conn.close()
