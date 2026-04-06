"""
Тести для RAR архівів
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.analyze_disk import analyze_archive


class TestRARArchives(unittest.TestCase):
    """Тести для RAR архівів"""

    def test_rar_detection_returns_type(self):
        """Тест що analyze_archive повертає type для RAR"""
        # Поки що тестуємо структуру відповіді
        result = analyze_archive('/nonexistent/file.rar')
        self.assertIn('type', result)
        self.assertIn('files_count', result)
        self.assertIn('uncompressed_size', result)
        self.assertIn('compression_ratio', result)
        self.assertIn('file_list', result)

    def test_non_rar_file_returns_none_type(self):
        """Тест що не-RAR файл повертає None type"""
        result = analyze_archive('/nonexistent/file.txt')
        self.assertIsNone(result['type'])
        self.assertEqual(result['files_count'], 0)


if __name__ == '__main__':
    unittest.main()
