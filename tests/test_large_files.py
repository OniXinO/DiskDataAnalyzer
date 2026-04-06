"""
Тести для пошуку великих файлів
"""

import unittest
import tempfile
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.large_files import find_large_files


class TestLargeFiles(unittest.TestCase):
    """Тести для пошуку великих файлів"""

    def setUp(self):
        """Створення тестової директорії"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Видалення тестової директорії"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_find_large_files_returns_list(self):
        """Тест що функція повертає список"""
        result = find_large_files(self.test_dir)
        self.assertIsInstance(result, list)

    def test_find_large_files_with_large_file(self):
        """Тест пошуку великого файлу"""
        # Створюємо файл 10MB
        large_file = os.path.join(self.test_dir, 'large.bin')
        with open(large_file, 'wb') as f:
            f.write(b'0' * (10 * 1024 * 1024))

        result = find_large_files(self.test_dir, min_size=5*1024*1024, limit=10)

        self.assertEqual(len(result), 1)
        self.assertGreaterEqual(result[0]['size'], 10*1024*1024)
        self.assertEqual(result[0]['name'], 'large.bin')
        self.assertIn('path', result[0])

    def test_find_large_files_ignores_small_files(self):
        """Тест що малі файли ігноруються"""
        # Створюємо малий файл
        small_file = os.path.join(self.test_dir, 'small.txt')
        with open(small_file, 'w') as f:
            f.write('small')

        result = find_large_files(self.test_dir, min_size=1*1024*1024, limit=10)

        self.assertEqual(len(result), 0)

    def test_find_large_files_sorted_by_size(self):
        """Тест що файли відсортовані за розміром"""
        # Створюємо файли різного розміру
        file1 = os.path.join(self.test_dir, 'file1.bin')
        file2 = os.path.join(self.test_dir, 'file2.bin')
        file3 = os.path.join(self.test_dir, 'file3.bin')

        with open(file1, 'wb') as f:
            f.write(b'0' * (5 * 1024 * 1024))  # 5MB
        with open(file2, 'wb') as f:
            f.write(b'0' * (10 * 1024 * 1024))  # 10MB
        with open(file3, 'wb') as f:
            f.write(b'0' * (7 * 1024 * 1024))  # 7MB

        result = find_large_files(self.test_dir, min_size=1*1024*1024, limit=10)

        self.assertEqual(len(result), 3)
        # Перевіряємо що відсортовано за спаданням
        self.assertGreaterEqual(result[0]['size'], result[1]['size'])
        self.assertGreaterEqual(result[1]['size'], result[2]['size'])

    def test_find_large_files_respects_limit(self):
        """Тест що ліміт працює"""
        # Створюємо 5 файлів
        for i in range(5):
            filepath = os.path.join(self.test_dir, f'file{i}.bin')
            with open(filepath, 'wb') as f:
                f.write(b'0' * (2 * 1024 * 1024))  # 2MB

        result = find_large_files(self.test_dir, min_size=1*1024*1024, limit=3)

        self.assertEqual(len(result), 3)


if __name__ == '__main__':
    unittest.main()
