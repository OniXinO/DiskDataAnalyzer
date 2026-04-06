"""
Тести для прогрес-бару
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.progress import ProgressBar


class TestProgressBar(unittest.TestCase):
    """Тести для ProgressBar"""

    def test_create_progress_bar(self):
        """Тест створення прогрес-бару"""
        pb = ProgressBar(total=100, desc="Test")
        self.assertEqual(pb.total, 100)
        self.assertEqual(pb.current, 0)
        self.assertEqual(pb.desc, "Test")
        pb.close()

    def test_update_progress(self):
        """Тест оновлення прогресу"""
        pb = ProgressBar(total=100, desc="Test")
        pb.update(50)
        self.assertEqual(pb.current, 50)
        pb.close()

    def test_update_multiple_times(self):
        """Тест множинних оновлень"""
        pb = ProgressBar(total=100, desc="Test")
        pb.update(25)
        pb.update(25)
        pb.update(25)
        self.assertEqual(pb.current, 75)
        pb.close()

    def test_update_beyond_total(self):
        """Тест оновлення понад total"""
        pb = ProgressBar(total=100, desc="Test")
        pb.update(150)
        self.assertEqual(pb.current, 100)
        pb.close()


if __name__ == '__main__':
    unittest.main()
