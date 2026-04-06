"""
Тести для модуля очищення диску
"""

import unittest
import os
import tempfile
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.cleanup import cleanup_duplicates, select_files_for_deletion


class TestCleanup(unittest.TestCase):
    """Тести для очищення диску"""

    def setUp(self):
        """Створення тимчасової директорії"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Видалення тимчасової директорії"""
        shutil.rmtree(self.test_dir)

    def test_cleanup_moves_duplicates_to_trash(self):
        """Тест що дублікати переміщуються в корзину"""
        # Створюємо дублікати
        file1 = os.path.join(self.test_dir, 'file1.txt')
        file2 = os.path.join(self.test_dir, 'file2.txt')

        with open(file1, 'w') as f:
            f.write('content')
        with open(file2, 'w') as f:
            f.write('content')

        duplicates = [{'files': [file1, file2]}]
        stats = cleanup_duplicates(duplicates, keep_first=True)

        self.assertTrue(os.path.exists(file1))
        self.assertFalse(os.path.exists(file2))
        self.assertEqual(stats['deleted'], 1)

    def test_cleanup_dry_run_does_not_delete(self):
        """Тест що dry_run не видаляє файли"""
        file1 = os.path.join(self.test_dir, 'file1.txt')
        file2 = os.path.join(self.test_dir, 'file2.txt')

        with open(file1, 'w') as f:
            f.write('content')
        with open(file2, 'w') as f:
            f.write('content')

        duplicates = [{'files': [file1, file2]}]
        stats = cleanup_duplicates(duplicates, keep_first=True, dry_run=True)

        self.assertTrue(os.path.exists(file1))
        self.assertTrue(os.path.exists(file2))
        self.assertEqual(stats['deleted'], 0)

    def test_select_files_for_deletion_returns_filtered_list(self):
        """Тест що select_files_for_deletion фільтрує файли"""
        duplicates = [
            {'files': ['/path/file1.txt', '/path/file2.txt', '/path/file3.txt']},
            {'files': ['/path/file4.txt', '/path/file5.txt']}
        ]

        # Користувач вибирає тільки деякі файли для видалення
        selected_indices = {0: [1], 1: [0]}  # group 0: file2, group 1: file4

        result = select_files_for_deletion(duplicates, selected_indices)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['files'], ['/path/file2.txt'])
        self.assertEqual(result[1]['files'], ['/path/file4.txt'])

    def test_cleanup_calculates_space_freed(self):
        """Тест що cleanup розраховує звільнений простір"""
        file1 = os.path.join(self.test_dir, 'file1.txt')
        file2 = os.path.join(self.test_dir, 'file2.txt')

        content = 'x' * 1000
        with open(file1, 'w') as f:
            f.write(content)
        with open(file2, 'w') as f:
            f.write(content)

        duplicates = [{'files': [file1, file2]}]
        stats = cleanup_duplicates(duplicates, keep_first=True)

        self.assertGreater(stats['space_freed'], 0)


if __name__ == '__main__':
    unittest.main()
