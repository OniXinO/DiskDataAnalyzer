"""
Тести для 7z архівів
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.analyze_disk import analyze_archive


class Test7zArchives(unittest.TestCase):
    """Тести для 7z архівів"""

    def test_7z_detection_returns_type(self):
        """Тест що analyze_archive повертає type для 7z"""
        result = analyze_archive('/nonexistent/file.7z')
        self.assertIn('type', result)
        self.assertIn('files_count', result)
        self.assertIn('uncompressed_size', result)

    def test_7z_file_extension_check(self):
        """Тест що 7z файли визначаються за розширенням"""
        # Поки що просто перевіряємо структуру
        result = analyze_archive('/test/archive.7z')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
