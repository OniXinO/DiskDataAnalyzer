"""
Базові тести для GUI вкладки порівняння папок
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gui.compare_tab import CompareTab


class TestCompareTab(unittest.TestCase):
    """Базові тести для CompareTab"""

    def test_compare_tab_can_be_imported(self):
        """Тест що CompareTab можна імпортувати"""
        self.assertTrue(hasattr(CompareTab, '__init__'))

    def test_compare_tab_has_required_methods(self):
        """Тест що CompareTab має необхідні методи"""
        required_methods = [
            '_create_widgets',
            '_select_folder',
            '_start_comparison',
            '_export_report'
        ]

        for method in required_methods:
            self.assertTrue(hasattr(CompareTab, method),
                          f"CompareTab missing method: {method}")


if __name__ == '__main__':
    unittest.main()
