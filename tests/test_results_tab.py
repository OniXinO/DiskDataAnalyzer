"""
Тести для вкладки результатів з візуалізацією
"""

import unittest
import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gui.tabs.results_tab import ResultsTab


class TestResultsTab(unittest.TestCase):
    """Тести для вкладки результатів"""

    def setUp(self):
        """Створення root вікна"""
        self.root = tk.Tk()

    def tearDown(self):
        """Закриття вікна"""
        self.root.destroy()

    def test_results_tab_creation(self):
        """Тест що вкладка створюється"""
        results = {'usage': {'total': 1000, 'used': 600, 'free': 400}}
        tab = ResultsTab(self.root, results)
        self.assertIsNotNone(tab)

    def test_results_tab_has_figure(self):
        """Тест що вкладка має matplotlib figure"""
        results = {'usage': {'total': 1000, 'used': 600, 'free': 400}}
        tab = ResultsTab(self.root, results)
        self.assertIsNotNone(tab.figure)

    def test_results_tab_has_canvas(self):
        """Тест що вкладка має canvas для відображення"""
        results = {'usage': {'total': 1000, 'used': 600, 'free': 400}}
        tab = ResultsTab(self.root, results)
        self.assertIsNotNone(tab.canvas)

    def test_results_tab_handles_empty_results(self):
        """Тест що вкладка обробляє порожні результати"""
        results = {}
        tab = ResultsTab(self.root, results)
        self.assertIsNotNone(tab)


if __name__ == '__main__':
    unittest.main()
