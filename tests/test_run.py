"""
Тест для run.py entry point
"""

import unittest
import os


class TestRun(unittest.TestCase):
    """Тести для run.py"""

    def test_run_file_exists(self):
        """Тест що run.py існує"""
        self.assertTrue(os.path.exists("run.py"))

    def test_run_has_main(self):
        """Тест що run.py має main функцію"""
        with open("run.py") as f:
            content = f.read()
            self.assertIn("def main()", content)
            self.assertIn("if __name__ == '__main__'", content)

    def test_run_imports_main_window(self):
        """Тест що run.py імпортує MainWindow"""
        with open("run.py") as f:
            content = f.read()
            self.assertIn("from src.gui.main_window import MainWindow", content)


if __name__ == '__main__':
    unittest.main()
