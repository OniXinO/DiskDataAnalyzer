"""
Тести для гібридного класифікатора файлів
"""

import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.file_classifier import FileClassifier


class TestFileClassifier(unittest.TestCase):
    """Тести для FileClassifier"""

    def setUp(self):
        """Створити тимчасову БД для кешу"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.classifier = FileClassifier(cache_db=self.temp_db.name)

    def tearDown(self):
        """Видалити тимчасову БД"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_classify_by_extension_exe(self):
        """Тест класифікації .exe файлу за розширенням"""
        result = self.classifier.classify("setup.exe", size=1024000, mtime=123456)

        self.assertEqual(result["category"], "installer")
        self.assertIn("description_uk", result)
        self.assertGreater(result["confidence"], 0.8)
        self.assertEqual(result["method"], "extension")

    def test_classify_by_extension_jpg(self):
        """Тест класифікації .jpg файлу за розширенням"""
        result = self.classifier.classify("photo.jpg", size=2048000, mtime=123456)

        self.assertEqual(result["category"], "image")
        self.assertEqual(result["method"], "extension")

    def test_classify_by_pattern_installer(self):
        """Тест класифікації за патерном в назві"""
        result = self.classifier.classify("installer_v2.bin", size=5000000, mtime=123456)

        self.assertEqual(result["category"], "installer")
        self.assertEqual(result["method"], "pattern")

    def test_classify_by_pattern_backup(self):
        """Тест класифікації backup файлу за патерном"""
        result = self.classifier.classify("data.backup", size=1024, mtime=123456)

        self.assertEqual(result["category"], "backup")
        self.assertEqual(result["method"], "pattern")

    def test_classify_uses_cache_on_second_call(self):
        """Тест що класифікатор використовує кеш при повторному виклику"""
        # Перший виклик
        result1 = self.classifier.classify("test.exe", size=1024, mtime=123456)

        # Другий виклик з тими ж параметрами
        result2 = self.classifier.classify("test.exe", size=1024, mtime=123456)

        self.assertEqual(result1["category"], result2["category"])
        # Другий виклик має бути з кешу
        self.assertTrue(result2.get("from_cache", False))

    def test_classify_cache_invalidates_on_size_change(self):
        """Тест що кеш інвалідується при зміні розміру"""
        # Перший виклик
        self.classifier.classify("test.exe", size=1024, mtime=123456)

        # Другий виклик зі зміненим розміром
        result = self.classifier.classify("test.exe", size=2048, mtime=123456)

        # Не має бути з кешу
        self.assertFalse(result.get("from_cache", False))

    def test_classify_unknown_extension_without_llm(self):
        """Тест класифікації невідомого розширення без LLM"""
        result = self.classifier.classify("unknown.xyz123", size=1024, mtime=123456,
                                         use_llm=False)

        self.assertEqual(result["category"], "other")
        self.assertEqual(result["method"], "fallback")

    def test_classify_with_llm_provider(self):
        """Тест класифікації через LLM провайдер"""
        # Mock LLM provider
        class MockLLMProvider:
            def classify_file(self, filename, context):
                return {
                    "category": "document",
                    "description_uk": "Документ Microsoft Word",
                    "confidence": 0.95
                }

        classifier = FileClassifier(cache_db=self.temp_db.name,
                                   llm_provider=MockLLMProvider())

        result = classifier.classify("report.xyz", size=1024, mtime=123456,
                                    use_llm=True)

        self.assertEqual(result["category"], "document")
        self.assertEqual(result["method"], "llm")
        self.assertIn("description_uk", result)

    def test_classify_respects_use_llm_flag(self):
        """Тест що use_llm=False блокує виклик LLM"""
        result = self.classifier.classify("unknown.xyz", size=1024, mtime=123456,
                                         use_llm=False)

        self.assertNotEqual(result["method"], "llm")

    def test_get_stats_returns_classification_stats(self):
        """Тест що get_stats повертає статистику класифікації"""
        self.classifier.classify("file1.exe", size=1024, mtime=123456)
        self.classifier.classify("file2.jpg", size=2048, mtime=123456)
        self.classifier.classify("file3.mp4", size=4096, mtime=123456)

        stats = self.classifier.get_stats()

        self.assertIn("total_classified", stats)
        self.assertIn("by_method", stats)
        self.assertIn("by_category", stats)
        self.assertEqual(stats["total_classified"], 3)

    def test_classify_handles_context_parameters(self):
        """Тест що класифікатор передає контекст в LLM"""
        class MockLLMProvider:
            def __init__(self):
                self.last_context = None

            def classify_file(self, filename, context):
                self.last_context = context
                return {
                    "category": "other",
                    "description_uk": "Файл",
                    "confidence": 0.5
                }

        mock_provider = MockLLMProvider()
        classifier = FileClassifier(cache_db=self.temp_db.name,
                                   llm_provider=mock_provider)

        classifier.classify("test.xyz", size=1024, mtime=123456,
                          parent_dir="/home/user/documents", use_llm=True)

        self.assertIsNotNone(mock_provider.last_context)
        self.assertEqual(mock_provider.last_context["size"], 1024)
        self.assertEqual(mock_provider.last_context["parent_dir"], "/home/user/documents")


if __name__ == '__main__':
    unittest.main()
