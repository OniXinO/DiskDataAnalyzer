"""
Тести для кольорового виводу CLI
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cli.colors import colorize, Colors, success, error, warning, info


class TestColors(unittest.TestCase):
    """Тести для кольорового виводу"""

    def test_colorize_with_color(self):
        """Тест colorize з кольором"""
        result = colorize("Test", Colors.GREEN)
        self.assertIn("Test", result)
        self.assertIsInstance(result, str)

    def test_success_message(self):
        """Тест success повідомлення"""
        result = success("Operation completed")
        self.assertIn("Operation completed", result)
        self.assertIn("✅", result)

    def test_error_message(self):
        """Тест error повідомлення"""
        result = error("Something failed")
        self.assertIn("Something failed", result)
        self.assertIn("❌", result)

    def test_warning_message(self):
        """Тест warning повідомлення"""
        result = warning("Be careful")
        self.assertIn("Be careful", result)
        self.assertIn("⚠️", result)

    def test_info_message(self):
        """Тест info повідомлення"""
        result = info("Information")
        self.assertIn("Information", result)
        self.assertIn("ℹ️", result)


if __name__ == '__main__':
    unittest.main()
