"""
Базові тести для GUI вкладки класифікатора
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gui.classifier_tab import ClassifierTab


class TestClassifierTab(unittest.TestCase):
    """Базові тести для ClassifierTab"""

    def test_classifier_tab_can_be_imported(self):
        """Тест що ClassifierTab можна імпортувати"""
        self.assertTrue(hasattr(ClassifierTab, '__init__'))

    def test_classifier_tab_has_required_methods(self):
        """Тест що ClassifierTab має необхідні методи"""
        required_methods = [
            '_create_widgets',
            '_select_folder',
            '_start_classification',
            '_export_csv',
            '_export_json'
        ]

        for method in required_methods:
            self.assertTrue(hasattr(ClassifierTab, method),
                          f"ClassifierTab missing method: {method}")


if __name__ == '__main__':
    unittest.main()
