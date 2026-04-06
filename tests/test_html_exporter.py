"""
Тести для HTML експортера
"""

import unittest
import tempfile
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from exporters.html_exporter import export_to_html


class TestHTMLExporter(unittest.TestCase):
    """Тести для HTML експортера"""

    def setUp(self):
        """Створення тестової директорії"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Видалення тестової директорії"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_export_creates_file(self):
        """Тест що експорт створює файл"""
        output_file = os.path.join(self.test_dir, 'report.html')
        data = {
            'title': 'Test Report',
            'summary': {'total_size': 1024}
        }

        export_to_html(data, output_file)

        self.assertTrue(os.path.exists(output_file))

    def test_export_valid_html(self):
        """Тест що експорт створює валідний HTML"""
        output_file = os.path.join(self.test_dir, 'report.html')
        data = {
            'title': 'Disk Analysis Report',
            'directory': '/test/path',
            'summary': {
                'total_size': 1024,
                'files_count': 10
            }
        }

        export_to_html(data, output_file)

        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Перевіряємо базову HTML структуру
        self.assertIn('<!DOCTYPE html>', content)
        self.assertIn('<html', content)
        self.assertIn('</html>', content)
        self.assertIn('<head>', content)
        self.assertIn('</head>', content)
        self.assertIn('<body>', content)
        self.assertIn('</body>', content)

    def test_export_contains_title(self):
        """Тест що HTML містить заголовок"""
        output_file = os.path.join(self.test_dir, 'report.html')
        data = {
            'title': 'My Custom Report Title',
            'summary': {}
        }

        export_to_html(data, output_file)

        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('My Custom Report Title', content)

    def test_export_contains_data(self):
        """Тест що HTML містить дані"""
        output_file = os.path.join(self.test_dir, 'report.html')
        data = {
            'title': 'Report',
            'directory': '/test/directory',
            'summary': {
                'total_size': 2048,
                'files_count': 25
            }
        }

        export_to_html(data, output_file)

        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('/test/directory', content)
        self.assertIn('2048', content)
        self.assertIn('25', content)

    def test_export_unicode_support(self):
        """Тест підтримки Unicode символів"""
        output_file = os.path.join(self.test_dir, 'report.html')
        data = {
            'title': 'Звіт аналізу диску',
            'directory': 'D:/Документи/Проєкти',
            'summary': {
                'description': 'Тестовий опис українською мовою'
            }
        }

        export_to_html(data, output_file)

        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('Звіт аналізу диску', content)
        self.assertIn('D:/Документи/Проєкти', content)
        self.assertIn('Тестовий опис українською мовою', content)


if __name__ == '__main__':
    unittest.main()
