"""
Базові тести для GUI вкладки дерева каталогів
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gui.tree_tab import TreeTab


class TestTreeTab(unittest.TestCase):
    """Базові тести для TreeTab"""

    def test_tree_tab_can_be_imported(self):
        """Тест що TreeTab можна імпортувати"""
        self.assertTrue(hasattr(TreeTab, '__init__'))

    def test_tree_tab_has_required_methods(self):
        """Тест що TreeTab має необхідні методи"""
        required_methods = [
            '_create_widgets',
            '_select_folder',
            '_start_build',
            '_export_text'
        ]

        for method in required_methods:
            self.assertTrue(hasattr(TreeTab, method),
                          f"TreeTab missing method: {method}")


if __name__ == '__main__':
    unittest.main()
