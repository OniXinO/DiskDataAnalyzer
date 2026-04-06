"""
Тести для порівняння папок
"""

import unittest
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.folder_compare import FolderCompare


class TestFolderCompare(unittest.TestCase):
    """Тести для FolderCompare"""

    def setUp(self):
        """Створити тимчасові структури для порівняння"""
        self.temp_dir1 = tempfile.mkdtemp()
        self.temp_dir2 = tempfile.mkdtemp()

        # Створити ідентичні файли в обох папках
        with open(os.path.join(self.temp_dir1, "same.txt"), 'w') as f:
            f.write("identical content")
        with open(os.path.join(self.temp_dir2, "same.txt"), 'w') as f:
            f.write("identical content")

        # Файл тільки в першій папці
        with open(os.path.join(self.temp_dir1, "only_in_first.txt"), 'w') as f:
            f.write("first only")

        # Файл тільки в другій папці
        with open(os.path.join(self.temp_dir2, "only_in_second.txt"), 'w') as f:
            f.write("second only")

        # Файли з однаковою назвою але різним вмістом
        with open(os.path.join(self.temp_dir1, "different.txt"), 'w') as f:
            f.write("content A")
        with open(os.path.join(self.temp_dir2, "different.txt"), 'w') as f:
            f.write("content B")

    def tearDown(self):
        """Видалити тимчасові структури"""
        if os.path.exists(self.temp_dir1):
            shutil.rmtree(self.temp_dir1)
        if os.path.exists(self.temp_dir2):
            shutil.rmtree(self.temp_dir2)

    def test_compare_returns_dict(self):
        """Тест що compare повертає словник"""
        comparer = FolderCompare(self.temp_dir1, self.temp_dir2)
        result = comparer.compare()

        self.assertIsInstance(result, dict)
        self.assertIn("identical", result)
        self.assertIn("different", result)
        self.assertIn("only_in_first", result)
        self.assertIn("only_in_second", result)

    def test_compare_detects_identical_files(self):
        """Тест виявлення ідентичних файлів"""
        comparer = FolderCompare(self.temp_dir1, self.temp_dir2)
        result = comparer.compare()

        self.assertIn("same.txt", result["identical"])

    def test_compare_detects_only_in_first(self):
        """Тест виявлення файлів тільки в першій папці"""
        comparer = FolderCompare(self.temp_dir1, self.temp_dir2)
        result = comparer.compare()

        self.assertIn("only_in_first.txt", result["only_in_first"])

    def test_compare_detects_only_in_second(self):
        """Тест виявлення файлів тільки в другій папці"""
        comparer = FolderCompare(self.temp_dir1, self.temp_dir2)
        result = comparer.compare()

        self.assertIn("only_in_second.txt", result["only_in_second"])

    def test_compare_detects_different_files(self):
        """Тест виявлення файлів з різним вмістом"""
        comparer = FolderCompare(self.temp_dir1, self.temp_dir2)
        result = comparer.compare()

        self.assertIn("different.txt", result["different"])

    def test_compare_with_hash_comparison(self):
        """Тест порівняння за hash"""
        comparer = FolderCompare(self.temp_dir1, self.temp_dir2, use_hash=True)
        result = comparer.compare()

        # Ідентичні файли мають бути виявлені за hash
        self.assertIn("same.txt", result["identical"])
        # Різні файли мають бути виявлені за hash
        self.assertIn("different.txt", result["different"])

    def test_compare_without_hash_uses_size_and_mtime(self):
        """Тест порівняння без hash (за розміром та часом)"""
        comparer = FolderCompare(self.temp_dir1, self.temp_dir2, use_hash=False)
        result = comparer.compare()

        # Має працювати навіть без hash
        self.assertIsInstance(result, dict)

    def test_compare_recursive(self):
        """Тест рекурсивного порівняння"""
        # Створити підпапки
        os.makedirs(os.path.join(self.temp_dir1, "subdir"))
        os.makedirs(os.path.join(self.temp_dir2, "subdir"))

        with open(os.path.join(self.temp_dir1, "subdir", "nested.txt"), 'w') as f:
            f.write("nested content")
        with open(os.path.join(self.temp_dir2, "subdir", "nested.txt"), 'w') as f:
            f.write("nested content")

        comparer = FolderCompare(self.temp_dir1, self.temp_dir2, recursive=True)
        result = comparer.compare()

        # Має знайти вкладений файл
        nested_files = [f for f in result["identical"] if "nested.txt" in f]
        self.assertGreater(len(nested_files), 0)

    def test_compare_non_recursive(self):
        """Тест не-рекурсивного порівняння"""
        # Створити підпапки
        os.makedirs(os.path.join(self.temp_dir1, "subdir"))
        os.makedirs(os.path.join(self.temp_dir2, "subdir"))

        with open(os.path.join(self.temp_dir1, "subdir", "nested.txt"), 'w') as f:
            f.write("nested")

        comparer = FolderCompare(self.temp_dir1, self.temp_dir2, recursive=False)
        result = comparer.compare()

        # Не має знаходити вкладені файли
        nested_files = [f for f in result["identical"] if "nested.txt" in f]
        self.assertEqual(len(nested_files), 0)

    def test_get_report_returns_string(self):
        """Тест що get_report повертає текстовий звіт"""
        comparer = FolderCompare(self.temp_dir1, self.temp_dir2)
        comparer.compare()

        report = comparer.get_report()

        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 0)

    def test_get_report_includes_statistics(self):
        """Тест що звіт містить статистику"""
        comparer = FolderCompare(self.temp_dir1, self.temp_dir2)
        comparer.compare()

        report = comparer.get_report()

        self.assertIn("identical", report.lower())
        self.assertIn("different", report.lower())

    def test_get_stats_returns_counts(self):
        """Тест що get_stats повертає підрахунки"""
        comparer = FolderCompare(self.temp_dir1, self.temp_dir2)
        comparer.compare()

        stats = comparer.get_stats()

        self.assertIn("identical_count", stats)
        self.assertIn("different_count", stats)
        self.assertIn("only_in_first_count", stats)
        self.assertIn("only_in_second_count", stats)
        self.assertIsInstance(stats["identical_count"], int)

    def test_compare_empty_directories(self):
        """Тест порівняння порожніх папок"""
        empty1 = tempfile.mkdtemp()
        empty2 = tempfile.mkdtemp()

        try:
            comparer = FolderCompare(empty1, empty2)
            result = comparer.compare()

            self.assertEqual(len(result["identical"]), 0)
            self.assertEqual(len(result["different"]), 0)
            self.assertEqual(len(result["only_in_first"]), 0)
            self.assertEqual(len(result["only_in_second"]), 0)
        finally:
            os.rmdir(empty1)
            os.rmdir(empty2)

    def test_compare_nonexistent_directory_raises_error(self):
        """Тест що неіснуюча папка викликає помилку"""
        with self.assertRaises(FileNotFoundError):
            comparer = FolderCompare("/nonexistent/path1", "/nonexistent/path2")
            comparer.compare()


if __name__ == '__main__':
    unittest.main()
