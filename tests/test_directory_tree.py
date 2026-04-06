"""
Тести для побудови дерева каталогів
"""

import unittest
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.directory_tree import DirectoryTree


class TestDirectoryTree(unittest.TestCase):
    """Тести для DirectoryTree"""

    def setUp(self):
        """Створити тимчасову структуру каталогів"""
        self.temp_dir = tempfile.mkdtemp()

        # Створити тестову структуру
        os.makedirs(os.path.join(self.temp_dir, "folder1", "subfolder1"))
        os.makedirs(os.path.join(self.temp_dir, "folder2"))
        os.makedirs(os.path.join(self.temp_dir, ".git"))  # Прихована папка

        # Створити файли
        open(os.path.join(self.temp_dir, "file1.txt"), 'w').close()
        open(os.path.join(self.temp_dir, "folder1", "file2.txt"), 'w').close()
        open(os.path.join(self.temp_dir, "folder1", "subfolder1", "file3.txt"), 'w').close()
        open(os.path.join(self.temp_dir, ".gitignore"), 'w').close()  # Прихований файл

    def tearDown(self):
        """Видалити тимчасову структуру"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_build_tree_returns_dict(self):
        """Тест що build_tree повертає словник"""
        tree = DirectoryTree(self.temp_dir)
        result = tree.build()

        self.assertIsInstance(result, dict)
        self.assertIn("name", result)
        self.assertIn("type", result)
        self.assertEqual(result["type"], "directory")

    def test_build_tree_includes_subdirectories(self):
        """Тест що дерево включає підкаталоги"""
        tree = DirectoryTree(self.temp_dir)
        result = tree.build()

        self.assertIn("children", result)
        self.assertGreater(len(result["children"]), 0)

        # Перевірити що є folder1
        folder_names = [child["name"] for child in result["children"] if child["type"] == "directory"]
        self.assertIn("folder1", folder_names)

    def test_build_tree_includes_files(self):
        """Тест що дерево включає файли"""
        tree = DirectoryTree(self.temp_dir)
        result = tree.build()

        file_names = [child["name"] for child in result["children"] if child["type"] == "file"]
        self.assertIn("file1.txt", file_names)

    def test_build_tree_recursive(self):
        """Тест що дерево будується рекурсивно"""
        tree = DirectoryTree(self.temp_dir)
        result = tree.build()

        # Знайти folder1
        folder1 = next((c for c in result["children"] if c["name"] == "folder1"), None)
        self.assertIsNotNone(folder1)

        # Перевірити що folder1 має children
        self.assertIn("children", folder1)

        # Перевірити що subfolder1 є в folder1
        subfolder_names = [c["name"] for c in folder1["children"] if c["type"] == "directory"]
        self.assertIn("subfolder1", subfolder_names)

    def test_build_tree_with_ignore_patterns(self):
        """Тест що ignore_patterns фільтрує файли/папки"""
        tree = DirectoryTree(self.temp_dir, ignore_patterns=[".git*"])
        result = tree.build()

        all_names = [child["name"] for child in result["children"]]

        # .git та .gitignore не повинні бути в результаті
        self.assertNotIn(".git", all_names)
        self.assertNotIn(".gitignore", all_names)

    def test_build_tree_with_max_depth(self):
        """Тест що max_depth обмежує глибину"""
        tree = DirectoryTree(self.temp_dir, max_depth=1)
        result = tree.build()

        # folder1 має бути
        folder1 = next((c for c in result["children"] if c["name"] == "folder1"), None)
        self.assertIsNotNone(folder1)

        # Але subfolder1 не має бути (глибина 2)
        if "children" in folder1:
            subfolder_names = [c["name"] for c in folder1["children"] if c["type"] == "directory"]
            self.assertEqual(len(subfolder_names), 0)

    def test_export_to_text_returns_string(self):
        """Тест що export_to_text повертає текстове представлення"""
        tree = DirectoryTree(self.temp_dir)
        tree.build()

        text = tree.export_to_text()

        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)
        self.assertIn("folder1", text)
        self.assertIn("file1.txt", text)

    def test_export_to_text_uses_tree_symbols(self):
        """Тест що експорт використовує символи дерева"""
        tree = DirectoryTree(self.temp_dir)
        tree.build()

        text = tree.export_to_text()

        # Має містити символи дерева
        self.assertTrue("├──" in text or "└──" in text or "│" in text)

    def test_get_stats_returns_statistics(self):
        """Тест що get_stats повертає статистику"""
        tree = DirectoryTree(self.temp_dir)
        tree.build()

        stats = tree.get_stats()

        self.assertIn("total_files", stats)
        self.assertIn("total_directories", stats)
        self.assertIn("total_size", stats)
        self.assertIsInstance(stats["total_files"], int)
        self.assertIsInstance(stats["total_directories"], int)

    def test_get_stats_counts_correctly(self):
        """Тест що статистика рахує правильно"""
        tree = DirectoryTree(self.temp_dir)
        tree.build()

        stats = tree.get_stats()

        # Маємо 3 файли (file1.txt, file2.txt, file3.txt)
        # .gitignore фільтрується за замовчуванням
        self.assertGreaterEqual(stats["total_files"], 3)

        # Маємо 3 папки (folder1, folder2, subfolder1)
        self.assertGreaterEqual(stats["total_directories"], 3)

    def test_build_empty_directory(self):
        """Тест побудови дерева для порожньої папки"""
        empty_dir = tempfile.mkdtemp()
        try:
            tree = DirectoryTree(empty_dir)
            result = tree.build()

            self.assertEqual(result["type"], "directory")
            self.assertEqual(len(result.get("children", [])), 0)
        finally:
            os.rmdir(empty_dir)

    def test_build_nonexistent_directory_raises_error(self):
        """Тест що неіснуюча папка викликає помилку"""
        with self.assertRaises(FileNotFoundError):
            tree = DirectoryTree("/nonexistent/path/xyz123")
            tree.build()


if __name__ == '__main__':
    unittest.main()
