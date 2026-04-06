"""
Тести для JSON експортера
"""

import unittest
import tempfile
import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from exporters.json_exporter import export_to_json


class TestJSONExporter(unittest.TestCase):
    """Тести для JSON експортера"""

    def setUp(self):
        """Створення тестової директорії"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Видалення тестової директорії"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_export_creates_file(self):
        """Тест що експорт створює файл"""
        output_file = os.path.join(self.test_dir, 'report.json')
        data = {'test': 'data'}

        export_to_json(data, output_file)

        self.assertTrue(os.path.exists(output_file))

    def test_export_valid_json(self):
        """Тест що експорт створює валідний JSON"""
        output_file = os.path.join(self.test_dir, 'report.json')
        data = {
            'directory': '/test/path',
            'total_size': 1024,
            'files_count': 10
        }

        export_to_json(data, output_file)

        with open(output_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        self.assertEqual(loaded_data, data)

    def test_export_nested_data(self):
        """Тест експорту вкладених структур"""
        output_file = os.path.join(self.test_dir, 'report.json')
        data = {
            'summary': {
                'total_size': 1024,
                'files': ['file1.txt', 'file2.txt']
            },
            'categories': {
                'documents': 512,
                'media': 512
            }
        }

        export_to_json(data, output_file)

        with open(output_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        self.assertEqual(loaded_data['summary']['total_size'], 1024)
        self.assertEqual(len(loaded_data['summary']['files']), 2)
        self.assertEqual(loaded_data['categories']['documents'], 512)

    def test_export_pretty_print(self):
        """Тест що JSON форматований з відступами"""
        output_file = os.path.join(self.test_dir, 'report.json')
        data = {'key': 'value', 'nested': {'inner': 'data'}}

        export_to_json(data, output_file)

        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Перевіряємо що є відступи (pretty print)
        self.assertIn('\n', content)
        self.assertIn('  ', content)

    def test_export_unicode_support(self):
        """Тест підтримки Unicode символів"""
        output_file = os.path.join(self.test_dir, 'report.json')
        data = {
            'name': 'Тестовий файл',
            'description': 'Опис українською мовою'
        }

        export_to_json(data, output_file)

        with open(output_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        self.assertEqual(loaded_data['name'], 'Тестовий файл')
        self.assertEqual(loaded_data['description'], 'Опис українською мовою')


if __name__ == '__main__':
    unittest.main()
