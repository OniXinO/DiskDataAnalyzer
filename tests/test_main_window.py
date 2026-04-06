"""
Тести для головного GUI вікна
"""

import unittest
import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gui.main_window import MainWindow


class TestMainWindow(unittest.TestCase):
    """Тести для головного вікна"""

    def setUp(self):
        """Створення root вікна"""
        self.root = tk.Tk()

    def tearDown(self):
        """Закриття вікна"""
        self.root.destroy()

    def test_window_creation(self):
        """Тест що вікно створюється"""
        window = MainWindow(self.root)
        self.assertIsNotNone(window)

    def test_window_has_title(self):
        """Тест що вікно має заголовок"""
        window = MainWindow(self.root)
        self.assertEqual(window.title, "DiskDataAnalyzer v0.6.0")
        self.assertEqual(self.root.title(), "DiskDataAnalyzer v0.6.0")

    def test_window_has_notebook(self):
        """Тест що вікно має notebook для вкладок"""
        window = MainWindow(self.root)
        self.assertIsNotNone(window.notebook)
        self.assertIsInstance(window.notebook, tk.Widget)


if __name__ == '__main__':
    unittest.main()
