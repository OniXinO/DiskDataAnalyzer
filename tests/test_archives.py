"""
Тести для аналізу архівів

Тестування функцій роботи з ZIP та TAR архівами
"""

import unittest
import os
import sys
import tempfile
import shutil
import zipfile
import tarfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.analyze_disk import analyze_archive


class TestAnalyzeArchive(unittest.TestCase):
    """Тести для аналізу архівів"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_zip_archive(self):
        # Створюємо ZIP архів
        zip_path = os.path.join(self.test_dir, 'test.zip')

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Додаємо файли
            zf.writestr('file1.txt', 'a' * 1000)
            zf.writestr('file2.txt', 'b' * 2000)
            zf.writestr('dir/file3.txt', 'c' * 500)

        result = analyze_archive(zip_path)

        self.assertEqual(result['type'], 'zip')
        self.assertEqual(result['files_count'], 3)
        self.assertEqual(result['uncompressed_size'], 3500)
        self.assertGreater(result['compression_ratio'], 0)
        self.assertEqual(len(result['file_list']), 3)

    def test_tar_archive(self):
        # Створюємо TAR архів
        tar_path = os.path.join(self.test_dir, 'test.tar')

        # Створюємо тимчасові файли для архівування
        temp_files_dir = os.path.join(self.test_dir, 'temp_files')
        os.makedirs(temp_files_dir)

        file1 = os.path.join(temp_files_dir, 'file1.txt')
        file2 = os.path.join(temp_files_dir, 'file2.txt')

        with open(file1, 'w') as f:
            f.write('a' * 1000)
        with open(file2, 'w') as f:
            f.write('b' * 2000)

        with tarfile.open(tar_path, 'w') as tf:
            tf.add(file1, arcname='file1.txt')
            tf.add(file2, arcname='file2.txt')

        result = analyze_archive(tar_path)

        self.assertEqual(result['type'], 'tar')
        self.assertEqual(result['files_count'], 2)
        self.assertGreaterEqual(result['uncompressed_size'], 3000)
        self.assertEqual(len(result['file_list']), 2)

    def test_tar_gz_archive(self):
        # Створюємо TAR.GZ архів
        tar_gz_path = os.path.join(self.test_dir, 'test.tar.gz')

        temp_files_dir = os.path.join(self.test_dir, 'temp_files')
        os.makedirs(temp_files_dir)

        file1 = os.path.join(temp_files_dir, 'file1.txt')
        with open(file1, 'w') as f:
            f.write('a' * 1000)

        with tarfile.open(tar_gz_path, 'w:gz') as tf:
            tf.add(file1, arcname='file1.txt')

        result = analyze_archive(tar_gz_path)

        self.assertEqual(result['type'], 'tar')
        self.assertEqual(result['files_count'], 1)
        self.assertGreaterEqual(result['uncompressed_size'], 1000)

    def test_empty_zip(self):
        # Створюємо порожній ZIP
        zip_path = os.path.join(self.test_dir, 'empty.zip')

        with zipfile.ZipFile(zip_path, 'w') as zf:
            pass

        result = analyze_archive(zip_path)

        self.assertEqual(result['type'], 'zip')
        self.assertEqual(result['files_count'], 0)
        self.assertEqual(result['uncompressed_size'], 0)

    def test_non_archive_file(self):
        # Створюємо звичайний текстовий файл
        text_file = os.path.join(self.test_dir, 'test.txt')
        with open(text_file, 'w') as f:
            f.write('Not an archive')

        result = analyze_archive(text_file)

        self.assertIsNone(result['type'])
        self.assertEqual(result['files_count'], 0)

    def test_nonexistent_file(self):
        result = analyze_archive('/nonexistent/archive.zip')

        self.assertIn('error', result)

    def test_compression_ratio_calculation(self):
        # Створюємо ZIP з високим стисненням
        zip_path = os.path.join(self.test_dir, 'compressed.zip')

        # Повторювані дані стискаються краще
        data = 'a' * 10000

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('file.txt', data)

        result = analyze_archive(zip_path)

        # Перевіряємо що стиснення відбулось
        self.assertGreater(result['compression_ratio'], 50)  # Мінімум 50% стиснення


class TestArchiveFileList(unittest.TestCase):
    """Тести для списку файлів в архіві"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_file_list_structure(self):
        zip_path = os.path.join(self.test_dir, 'test.zip')

        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr('file1.txt', 'content1')
            zf.writestr('dir/file2.txt', 'content2')

        result = analyze_archive(zip_path)

        self.assertEqual(len(result['file_list']), 2)

        # Перевіряємо структуру першого файлу
        file1 = result['file_list'][0]
        self.assertIn('name', file1)
        self.assertIn('size', file1)
        self.assertIn('compressed', file1)

    def test_file_sizes_in_list(self):
        zip_path = os.path.join(self.test_dir, 'test.zip')

        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr('small.txt', 'a' * 100)
            zf.writestr('large.txt', 'b' * 1000)

        result = analyze_archive(zip_path)

        # Знаходимо файли за назвою
        small_file = next(f for f in result['file_list'] if 'small.txt' in f['name'])
        large_file = next(f for f in result['file_list'] if 'large.txt' in f['name'])

        self.assertEqual(small_file['size'], 100)
        self.assertEqual(large_file['size'], 1000)


if __name__ == '__main__':
    unittest.main()
