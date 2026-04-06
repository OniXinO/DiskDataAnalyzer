"""
Тести для кешу класифікації файлів
"""

import unittest
import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.classification_cache import ClassificationCache


class TestClassificationCache(unittest.TestCase):
    """Тести для ClassificationCache"""

    def setUp(self):
        """Створити тимчасову БД для тестів"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.cache = ClassificationCache(self.temp_db.name)

    def tearDown(self):
        """Видалити тимчасову БД"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_cache_miss_returns_none(self):
        """Тест що кеш повертає None для відсутнього файлу"""
        result = self.cache.get("nonexistent.txt", size=1024, mtime=123456)
        self.assertIsNone(result)

    def test_cache_stores_and_retrieves_result(self):
        """Тест що кеш зберігає та повертає результат"""
        classification = {
            "category": "document",
            "description_uk": "Текстовий документ",
            "confidence": 0.95
        }

        self.cache.set("test.txt", size=1024, mtime=123456,
                      provider="claude", result=classification)

        cached = self.cache.get("test.txt", size=1024, mtime=123456)

        self.assertIsNotNone(cached)
        self.assertEqual(cached["category"], "document")
        self.assertEqual(cached["description_uk"], "Текстовий документ")
        self.assertEqual(cached["confidence"], 0.95)
        self.assertEqual(cached["provider"], "claude")

    def test_cache_invalidates_on_size_change(self):
        """Тест що кеш інвалідується при зміні розміру файлу"""
        classification = {
            "category": "document",
            "description_uk": "Текстовий документ",
            "confidence": 0.95
        }

        self.cache.set("test.txt", size=1024, mtime=123456,
                      provider="claude", result=classification)

        # Змінений розмір - кеш не повинен повернути результат
        cached = self.cache.get("test.txt", size=2048, mtime=123456)
        self.assertIsNone(cached)

    def test_cache_invalidates_on_mtime_change(self):
        """Тест що кеш інвалідується при зміні часу модифікації"""
        classification = {
            "category": "document",
            "description_uk": "Текстовий документ",
            "confidence": 0.95
        }

        self.cache.set("test.txt", size=1024, mtime=123456,
                      provider="claude", result=classification)

        # Змінений mtime - кеш не повинен повернути результат
        cached = self.cache.get("test.txt", size=1024, mtime=789012)
        self.assertIsNone(cached)

    def test_cache_stores_provider_name(self):
        """Тест що кеш зберігає ім'я провайдера"""
        classification = {
            "category": "image",
            "description_uk": "Зображення",
            "confidence": 0.9
        }

        self.cache.set("photo.jpg", size=2048, mtime=123456,
                      provider="openai", result=classification)

        cached = self.cache.get("photo.jpg", size=2048, mtime=123456)
        self.assertEqual(cached["provider"], "openai")

    def test_cache_stores_timestamp(self):
        """Тест що кеш зберігає час створення запису"""
        classification = {
            "category": "video",
            "description_uk": "Відео файл",
            "confidence": 0.85
        }

        before = time.time()
        self.cache.set("video.mp4", size=10240, mtime=123456,
                      provider="ollama", result=classification)
        after = time.time()

        cached = self.cache.get("video.mp4", size=10240, mtime=123456)

        self.assertIn("cached_at", cached)
        self.assertGreaterEqual(cached["cached_at"], before)
        self.assertLessEqual(cached["cached_at"], after)

    def test_cache_handles_multiple_files(self):
        """Тест що кеш коректно працює з кількома файлами"""
        files = [
            ("file1.txt", 1024, 111111, "document"),
            ("file2.jpg", 2048, 222222, "image"),
            ("file3.mp4", 4096, 333333, "video")
        ]

        for filename, size, mtime, category in files:
            self.cache.set(filename, size=size, mtime=mtime,
                          provider="claude", result={"category": category})

        for filename, size, mtime, category in files:
            cached = self.cache.get(filename, size=size, mtime=mtime)
            self.assertIsNotNone(cached)
            self.assertEqual(cached["category"], category)

    def test_cache_clear_removes_all_entries(self):
        """Тест що clear() видаляє всі записи"""
        self.cache.set("file1.txt", size=1024, mtime=123456,
                      provider="claude", result={"category": "document"})
        self.cache.set("file2.jpg", size=2048, mtime=789012,
                      provider="openai", result={"category": "image"})

        self.cache.clear()

        self.assertIsNone(self.cache.get("file1.txt", size=1024, mtime=123456))
        self.assertIsNone(self.cache.get("file2.jpg", size=2048, mtime=789012))

    def test_cache_get_stats_returns_correct_counts(self):
        """Тест що get_stats() повертає правильну статистику"""
        stats = self.cache.get_stats()
        self.assertEqual(stats["total_entries"], 0)

        self.cache.set("file1.txt", size=1024, mtime=123456,
                      provider="claude", result={"category": "document"})
        self.cache.set("file2.jpg", size=2048, mtime=789012,
                      provider="openai", result={"category": "image"})

        stats = self.cache.get_stats()
        self.assertEqual(stats["total_entries"], 2)
        self.assertIn("claude", stats["by_provider"])
        self.assertIn("openai", stats["by_provider"])


if __name__ == '__main__':
    unittest.main()
