"""
Базові тести для GUI вкладки детектора сміття
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gui.junk_tab import JunkTab


class TestJunkTab(unittest.TestCase):
    """Базові тести для JunkTab"""

    def test_junk_tab_can_be_imported(self):
        """Тест що JunkTab можна імпортувати"""
        self.assertTrue(hasattr(JunkTab, '__init__'))

    def test_junk_tab_has_required_methods(self):
        """Тест що JunkTab має необхідні методи"""
        required_methods = [
            '_create_widgets',
            '_select_folder',
            '_start_scan',
            '_safe_delete'
        ]

        for method in required_methods:
            self.assertTrue(hasattr(JunkTab, method),
                          f"JunkTab missing method: {method}")


if __name__ == '__main__':
    unittest.main()
