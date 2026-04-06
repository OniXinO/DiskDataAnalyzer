"""
Тести для вкладки експорту результатів
"""

import unittest
import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gui.tabs.export_tab import ExportTab


class TestExportTab(unittest.TestCase):
    """Тести для вкладки експорту"""

    def setUp(self):
        """Створення root вікна"""
        self.root = tk.Tk()
        self.results = {
            'usage': {'total': 1000, 'used': 600, 'free': 400},
            'largest_files': [
                {'path': '/test/file1.txt', 'size': 100},
                {'path': '/test/file2.txt', 'size': 50}
            ]
        }

    def tearDown(self):
        """Закриття вікна"""
        self.root.destroy()

    def test_export_tab_creation(self):
        """Тест що вкладка створюється"""
        tab = ExportTab(self.root, self.results)
        self.assertIsNotNone(tab)

    def test_export_tab_has_format_selection(self):
        """Тест що вкладка має вибір формату"""
        tab = ExportTab(self.root, self.results)
        self.assertIsNotNone(tab.format_var)
        self.assertIn(tab.format_var.get(), ['JSON', 'CSV', 'HTML'])

    def test_export_tab_has_export_button(self):
        """Тест що вкладка має кнопку експорту"""
        tab = ExportTab(self.root, self.results)
        self.assertIsNotNone(tab.export_btn)

    def test_export_tab_handles_empty_results(self):
        """Тест що вкладка обробляє порожні результати"""
        tab = ExportTab(self.root, {})
        self.assertIsNotNone(tab)


if __name__ == '__main__':
    unittest.main()
