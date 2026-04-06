"""
Інтеграційні тести для MainWindow з новими вкладками
"""

import unittest
import os
import sys
import tkinter as tk

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gui.main_window import MainWindow


class TestMainWindowIntegration(unittest.TestCase):
    """Тести інтеграції MainWindow з новими вкладками"""

    def setUp(self):
        """Створити тестове вікно"""
        self.root = tk.Tk()
        self.window = MainWindow(self.root)

    def tearDown(self):
        """Закрити тестове вікно"""
        self.root.destroy()

    def test_has_classifier_tab(self):
        """Тест що є вкладка File Classifier"""
        tabs = [self.window.notebook.tab(i, "text")
                for i in range(self.window.notebook.index("end"))]
        self.assertIn("File Classifier", tabs)

    def test_has_tree_tab(self):
        """Тест що є вкладка Directory Tree"""
        tabs = [self.window.notebook.tab(i, "text")
                for i in range(self.window.notebook.index("end"))]
        self.assertIn("Directory Tree", tabs)

    def test_has_compare_tab(self):
        """Тест що є вкладка Folder Compare"""
        tabs = [self.window.notebook.tab(i, "text")
                for i in range(self.window.notebook.index("end"))]
        self.assertIn("Folder Compare", tabs)

    def test_has_junk_tab(self):
        """Тест що є вкладка Junk Detector"""
        tabs = [self.window.notebook.tab(i, "text")
                for i in range(self.window.notebook.index("end"))]
        self.assertIn("Junk Detector", tabs)

    def test_all_tabs_accessible(self):
        """Тест що всі вкладки доступні"""
        num_tabs = self.window.notebook.index("end")
        self.assertEqual(num_tabs, 4, "Should have 4 tabs")

    def test_tab_switching(self):
        """Тест що можна перемикатися між вкладками"""
        # Switch to each tab
        for i in range(self.window.notebook.index("end")):
            self.window.notebook.select(i)
            selected = self.window.notebook.index("current")
            self.assertEqual(selected, i)


if __name__ == '__main__':
    unittest.main()
