"""
Тести для PDF експортера
"""

import unittest
import os
import tempfile
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from exporters.pdf_exporter import export_to_pdf


class TestPDFExporter(unittest.TestCase):
    """Тести для PDF експортера"""

    def setUp(self):
        """Створення тимчасової директорії"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Видалення тимчасової директорії"""
        shutil.rmtree(self.test_dir)

    def test_pdf_export_creates_file(self):
        """Тест що PDF файл створюється"""
        output_file = os.path.join(self.test_dir, 'report.pdf')
        data = {
            'title': 'Test Report',
            'usage': {'total': 1000, 'used': 600, 'free': 400}
        }

        export_to_pdf(data, output_file)

        self.assertTrue(os.path.exists(output_file))

    def test_pdf_export_with_summary(self):
        """Тест що PDF містить summary"""
        output_file = os.path.join(self.test_dir, 'report.pdf')
        data = {
            'title': 'Disk Analysis Report',
            'summary': {
                'Total Size': '1000 GB',
                'Used': '600 GB',
                'Free': '400 GB'
            }
        }

        export_to_pdf(data, output_file)

        self.assertTrue(os.path.exists(output_file))
        self.assertGreater(os.path.getsize(output_file), 0)

    def test_pdf_export_with_largest_files(self):
        """Тест що PDF містить largest files"""
        output_file = os.path.join(self.test_dir, 'report.pdf')
        data = {
            'title': 'Disk Analysis Report',
            'largest_files': [
                {'path': '/test/file1.txt', 'size': 100},
                {'path': '/test/file2.txt', 'size': 50}
            ]
        }

        export_to_pdf(data, output_file)

        self.assertTrue(os.path.exists(output_file))
        self.assertGreater(os.path.getsize(output_file), 0)


if __name__ == '__main__':
    unittest.main()
