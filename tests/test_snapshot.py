"""
Тести для порівняння знімків диску
"""

import unittest
import os
import tempfile
import shutil
import json
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.snapshot import create_snapshot, compare_snapshots


class TestSnapshot(unittest.TestCase):
    """Тести для знімків диску"""

    def setUp(self):
        """Створення тимчасової директорії"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Видалення тимчасової директорії"""
        shutil.rmtree(self.test_dir)

    def test_create_snapshot_creates_file(self):
        """Тест що create_snapshot створює файл"""
        output_file = os.path.join(self.test_dir, 'snapshot.json')

        snapshot = create_snapshot(self.test_dir, output_file)

        self.assertTrue(os.path.exists(output_file))
        self.assertIn('timestamp', snapshot)
        self.assertIn('drive', snapshot)

    def test_compare_snapshots_detects_added_directories(self):
        """Тест що compare_snapshots виявляє додані директорії"""
        snapshot1 = {
            'timestamp': '2026-04-01',
            'top_directories': [
                {'path': '/dir1', 'size': 100}
            ]
        }
        snapshot2 = {
            'timestamp': '2026-04-06',
            'top_directories': [
                {'path': '/dir1', 'size': 100},
                {'path': '/dir2', 'size': 200}
            ]
        }

        diff = compare_snapshots(snapshot1, snapshot2)

        self.assertIn('added', diff)
        self.assertEqual(diff['added'], ['/dir2'])

    def test_compare_snapshots_detects_removed_directories(self):
        """Тест що compare_snapshots виявляє видалені директорії"""
        snapshot1 = {
            'timestamp': '2026-04-01',
            'top_directories': [
                {'path': '/dir1', 'size': 100},
                {'path': '/dir2', 'size': 200}
            ]
        }
        snapshot2 = {
            'timestamp': '2026-04-06',
            'top_directories': [
                {'path': '/dir1', 'size': 100}
            ]
        }

        diff = compare_snapshots(snapshot1, snapshot2)

        self.assertIn('removed', diff)
        self.assertEqual(diff['removed'], ['/dir2'])

    def test_compare_snapshots_detects_modified_directories(self):
        """Тест що compare_snapshots виявляє змінені директорії"""
        snapshot1 = {
            'timestamp': '2026-04-01',
            'top_directories': [
                {'path': '/dir1', 'size': 100}
            ]
        }
        snapshot2 = {
            'timestamp': '2026-04-06',
            'top_directories': [
                {'path': '/dir1', 'size': 150}
            ]
        }

        diff = compare_snapshots(snapshot1, snapshot2)

        self.assertIn('modified', diff)
        self.assertEqual(len(diff['modified']), 1)
        self.assertEqual(diff['modified'][0]['path'], '/dir1')
        self.assertEqual(diff['modified'][0]['change'], 50)

    def test_compare_snapshots_calculates_size_change(self):
        """Тест що compare_snapshots розраховує зміну розміру"""
        snapshot1 = {
            'timestamp': '2026-04-01',
            'usage': {'used': 1000}
        }
        snapshot2 = {
            'timestamp': '2026-04-06',
            'usage': {'used': 1500}
        }

        diff = compare_snapshots(snapshot1, snapshot2)

        self.assertIn('size_change', diff)
        self.assertEqual(diff['size_change'], 500)


if __name__ == '__main__':
    unittest.main()
