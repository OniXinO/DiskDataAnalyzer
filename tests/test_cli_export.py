"""
Тести для CLI з експортом звітів
"""

import unittest
import tempfile
import os
import sys
import json
import csv
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestCLIExport(unittest.TestCase):
    """Тести для CLI експорту"""

    def setUp(self):
        """Створення тестової директорії"""
        self.test_dir = tempfile.mkdtemp()
        self.script_path = os.path.join(
            os.path.dirname(__file__), '..', 'src', 'core', 'analyze_disk.py'
        )

    def tearDown(self):
        """Видалення тестової директорії"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_export_json_creates_file(self):
        """Тест що --export json створює JSON файл"""
        output_file = os.path.join(self.test_dir, 'report.json')

        result = subprocess.run([
            sys.executable, self.script_path,
            self.test_dir,
            '--export', 'json',
            '--output', output_file
        ], capture_output=True, text=True)

        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(output_file))

    def test_export_json_valid_format(self):
        """Тест що JSON файл валідний"""
        output_file = os.path.join(self.test_dir, 'report.json')

        subprocess.run([
            sys.executable, self.script_path,
            self.test_dir,
            '--export', 'json',
            '--output', output_file
        ], capture_output=True)

        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertIsInstance(data, dict)
        self.assertIn('drive', data)

    def test_export_csv_creates_file(self):
        """Тест що --export csv створює CSV файл"""
        output_file = os.path.join(self.test_dir, 'report.csv')

        result = subprocess.run([
            sys.executable, self.script_path,
            self.test_dir,
            '--export', 'csv',
            '--output', output_file
        ], capture_output=True, text=True)

        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(output_file))

    def test_export_html_creates_file(self):
        """Тест що --export html створює HTML файл"""
        output_file = os.path.join(self.test_dir, 'report.html')

        result = subprocess.run([
            sys.executable, self.script_path,
            self.test_dir,
            '--export', 'html',
            '--output', output_file
        ], capture_output=True, text=True)

        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(output_file))

    def test_export_html_valid_format(self):
        """Тест що HTML файл валідний"""
        output_file = os.path.join(self.test_dir, 'report.html')

        subprocess.run([
            sys.executable, self.script_path,
            self.test_dir,
            '--export', 'html',
            '--output', output_file
        ], capture_output=True)

        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('<!DOCTYPE html>', content)
        self.assertIn('</html>', content)

    def test_invalid_export_format(self):
        """Тест що невалідний формат повертає помилку"""
        output_file = os.path.join(self.test_dir, 'report.txt')

        result = subprocess.run([
            sys.executable, self.script_path,
            self.test_dir,
            '--export', 'invalid',
            '--output', output_file
        ], capture_output=True, text=True)

        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
