"""
Тести для вкладки вибору диску
"""

import unittest
import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gui.tabs.drive_tab import DriveTab


class TestDriveTab(unittest.TestCase):
    """Тести для вкладки вибору диску"""

    def setUp(self):
        """Створення root вікна"""
        self.root = tk.Tk()

    def tearDown(self):
        """Закриття вікна"""
        self.root.destroy()

    def test_drive_tab_creation(self):
        """Тест що вкладка створюється"""
        tab = DriveTab(self.root)
        self.assertIsNotNone(tab)

    def test_drive_tab_lists_drives(self):
        """Тест що вкладка показує список дисків"""
        tab = DriveTab(self.root)
        drives = tab.get_available_drives()
        self.assertIsInstance(drives, list)
        # На Windows має бути хоча б один диск
        self.assertGreater(len(drives), 0)

    def test_drive_tab_has_combobox(self):
        """Тест що вкладка має combobox для вибору"""
        tab = DriveTab(self.root)
        self.assertIsNotNone(tab.drive_combo)
        self.assertIsNotNone(tab.drive_var)

    def test_drive_tab_has_analyze_button(self):
        """Тест що вкладка має кнопку аналізу"""
        tab = DriveTab(self.root)
        self.assertIsNotNone(tab.analyze_btn)


if __name__ == '__main__':
    unittest.main()
