"""
Unit тести для DiskDataAnalyzer

Тестування основних функцій аналізу дисків
"""

import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Додаємо src до шляху
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.analyze_disk import (
    get_disk_usage,
    format_bytes,
    get_directory_size,
    calculate_file_hash,
    categorize_directory
)


class TestFormatBytes(unittest.TestCase):
    """Тести для форматування байтів"""

    def test_bytes(self):
        self.assertEqual(format_bytes(100), "100.00 B")

    def test_kilobytes(self):
        self.assertEqual(format_bytes(1024), "1.00 KB")

    def test_megabytes(self):
        self.assertEqual(format_bytes(1024 * 1024), "1.00 MB")

    def test_gigabytes(self):
        self.assertEqual(format_bytes(1024 * 1024 * 1024), "1.00 GB")

    def test_terabytes(self):
        self.assertEqual(format_bytes(1024 * 1024 * 1024 * 1024), "1.00 TB")

    def test_zero(self):
        self.assertEqual(format_bytes(0), "0.00 B")


class TestGetDiskUsage(unittest.TestCase):
    """Тести для отримання інформації про диск"""

    def test_valid_path(self):
        # Тестуємо на поточній директорії
        result = get_disk_usage('.')
        self.assertIn('total', result)
        self.assertIn('used', result)
        self.assertIn('free', result)
        self.assertIn('percent', result)
        self.assertGreater(result['total'], 0)
        self.assertGreaterEqual(result['used'], 0)
        self.assertGreaterEqual(result['free'], 0)
        self.assertGreaterEqual(result['percent'], 0)
        self.assertLessEqual(result['percent'], 100)

    def test_invalid_path(self):
        # Тестуємо на неіснуючому шляху
        result = get_disk_usage('/nonexistent/path/12345')
        self.assertIn('error', result)


class TestGetDirectorySize(unittest.TestCase):
    """Тести для розрахунку розміру директорії"""

    def setUp(self):
        # Створюємо тимчасову директорію для тестів
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Видаляємо тимчасову директорію
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_empty_directory(self):
        size = get_directory_size(self.test_dir)
        self.assertEqual(size, 0)

    def test_directory_with_files(self):
        # Створюємо файли
        file1 = os.path.join(self.test_dir, 'file1.txt')
        file2 = os.path.join(self.test_dir, 'file2.txt')

        with open(file1, 'w') as f:
            f.write('a' * 1000)  # 1000 байт

        with open(file2, 'w') as f:
            f.write('b' * 2000)  # 2000 байт

        size = get_directory_size(self.test_dir)
        self.assertGreaterEqual(size, 3000)  # Мінімум 3000 байт

    def test_nested_directories(self):
        # Створюємо вкладені директорії
        subdir = os.path.join(self.test_dir, 'subdir')
        os.makedirs(subdir)

        file1 = os.path.join(self.test_dir, 'file1.txt')
        file2 = os.path.join(subdir, 'file2.txt')

        with open(file1, 'w') as f:
            f.write('a' * 1000)

        with open(file2, 'w') as f:
            f.write('b' * 1000)

        size = get_directory_size(self.test_dir)
        self.assertGreaterEqual(size, 2000)

    def test_nonexistent_directory(self):
        size = get_directory_size('/nonexistent/path/12345')
        self.assertEqual(size, 0)


class TestCalculateFileHash(unittest.TestCase):
    """Тести для обчислення хешу файлу"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_md5_hash(self):
        # Створюємо файл з відомим вмістом
        test_file = os.path.join(self.test_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('Hello, World!')

        hash_result = calculate_file_hash(test_file, 'md5')
        # MD5 хеш для "Hello, World!"
        expected = '65a8e27d8879283831b664bd8b7f0ad4'
        self.assertEqual(hash_result, expected)

    def test_sha256_hash(self):
        test_file = os.path.join(self.test_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('Hello, World!')

        hash_result = calculate_file_hash(test_file, 'sha256')
        # SHA256 хеш для "Hello, World!"
        expected = 'dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f'
        self.assertEqual(hash_result, expected)

    def test_nonexistent_file(self):
        hash_result = calculate_file_hash('/nonexistent/file.txt', 'md5')
        self.assertIsNone(hash_result)

    def test_empty_file(self):
        test_file = os.path.join(self.test_dir, 'empty.txt')
        Path(test_file).touch()

        hash_result = calculate_file_hash(test_file, 'md5')
        # MD5 хеш для порожнього файлу
        expected = 'd41d8cd98f00b204e9800998ecf8427e'
        self.assertEqual(hash_result, expected)


class TestCategorizeDirectory(unittest.TestCase):
    """Тести для категоризації директорій"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_project_directory_with_git(self):
        # Створюємо .git директорію
        git_dir = os.path.join(self.test_dir, '.git')
        os.makedirs(git_dir)

        result = categorize_directory(self.test_dir)
        self.assertEqual(result['category'], 'project')
        self.assertGreater(result['confidence'], 70)
        self.assertIn('.git', result['markers_found'])

    def test_project_directory_with_package_json(self):
        # Створюємо package.json
        package_json = os.path.join(self.test_dir, 'package.json')
        with open(package_json, 'w') as f:
            f.write('{}')

        result = categorize_directory(self.test_dir)
        self.assertEqual(result['category'], 'project')
        self.assertGreater(result['confidence'], 70)

    def test_backup_directory_by_name(self):
        # Створюємо директорію з назвою "backup"
        backup_dir = os.path.join(self.test_dir, 'backup_2026')
        os.makedirs(backup_dir)

        result = categorize_directory(backup_dir)
        self.assertEqual(result['category'], 'backup')

    def test_empty_directory(self):
        result = categorize_directory(self.test_dir)
        self.assertEqual(result['category'], 'unknown')
        self.assertEqual(result['confidence'], 0)

    def test_nonexistent_directory(self):
        result = categorize_directory('/nonexistent/path/12345')
        self.assertEqual(result['category'], 'unknown')


if __name__ == '__main__':
    unittest.main()
