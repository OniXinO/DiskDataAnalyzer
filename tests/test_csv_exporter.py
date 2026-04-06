"""
Тести для CSV експортера
"""

import unittest
import tempfile
import os
import sys
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from exporters.csv_exporter import export_to_csv


class TestCSVExporter(unittest.TestCase):
    """Тести для CSV експортера"""

    def setUp(self):
        """Створення тестової директорії"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Видалення тестової директорії"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_export_creates_file(self):
        """Тест що експорт створює файл"""
        output_file = os.path.join(self.test_dir, 'report.csv')
        data = [
            {'name': 'file1.txt', 'size': 1024},
            {'name': 'file2.txt', 'size': 2048}
        ]

        export_to_csv(data, output_file)

        self.assertTrue(os.path.exists(output_file))

    def test_export_valid_csv(self):
        """Тест що експорт створює валідний CSV"""
        output_file = os.path.join(self.test_dir, 'report.csv')
        data = [
            {'name': 'file1.txt', 'size': 1024, 'type': 'text'},
            {'name': 'file2.txt', 'size': 2048, 'type': 'text'}
        ]

        export_to_csv(data, output_file)

        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['name'], 'file1.txt')
        self.assertEqual(rows[0]['size'], '1024')
        self.assertEqual(rows[1]['name'], 'file2.txt')

    def test_export_headers(self):
        """Тест що CSV містить заголовки"""
        output_file = os.path.join(self.test_dir, 'report.csv')
        data = [
            {'name': 'file1.txt', 'size': 1024},
            {'name': 'file2.txt', 'size': 2048}
        ]

        export_to_csv(data, output_file)

        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)

        self.assertIn('name', headers)
        self.assertIn('size', headers)

    def test_export_unicode_support(self):
        """Тест підтримки Unicode символів"""
        output_file = os.path.join(self.test_dir, 'report.csv')
        data = [
            {'name': 'Тестовий файл.txt', 'description': 'Опис українською'},
            {'name': 'Другий файл.doc', 'description': 'Ще один опис'}
        ]

        export_to_csv(data, output_file)

        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(rows[0]['name'], 'Тестовий файл.txt')
        self.assertEqual(rows[0]['description'], 'Опис українською')

    def test_export_empty_list(self):
        """Тест експорту порожнього списку"""
        output_file = os.path.join(self.test_dir, 'report.csv')
        data = []

        export_to_csv(data, output_file)

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # Порожній файл або тільки заголовки
        self.assertEqual(content.strip(), '')


if __name__ == '__main__':
    unittest.main()
