"""
Тести для планувальника аналізу диску
"""

import unittest
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.scheduler import DiskScheduler


class TestScheduler(unittest.TestCase):
    """Тести для планувальника"""

    def setUp(self):
        """Створення scheduler"""
        self.scheduler = DiskScheduler()

    def tearDown(self):
        """Зупинка scheduler"""
        self.scheduler.shutdown()

    def test_scheduler_creates_job(self):
        """Тест що scheduler створює job"""
        job = self.scheduler.schedule_analysis(
            drive='C:',
            interval_hours=24,
            report_dir='O:/reports'
        )

        self.assertIsNotNone(job)
        self.assertEqual(job.id, 'analysis_C:')

    def test_scheduler_lists_jobs(self):
        """Тест що scheduler показує список jobs"""
        self.scheduler.schedule_analysis(
            drive='C:',
            interval_hours=24,
            report_dir='O:/reports'
        )

        jobs = self.scheduler.list_jobs()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].id, 'analysis_C:')

    def test_scheduler_removes_job(self):
        """Тест що scheduler видаляє job"""
        self.scheduler.schedule_analysis(
            drive='C:',
            interval_hours=24,
            report_dir='O:/reports'
        )

        self.scheduler.remove_job('C:')
        jobs = self.scheduler.list_jobs()
        self.assertEqual(len(jobs), 0)

    def test_scheduler_replaces_existing_job(self):
        """Тест що scheduler замінює існуючий job"""
        self.scheduler.schedule_analysis(
            drive='C:',
            interval_hours=24,
            report_dir='O:/reports'
        )

        self.scheduler.schedule_analysis(
            drive='C:',
            interval_hours=12,
            report_dir='O:/reports'
        )

        jobs = self.scheduler.list_jobs()
        self.assertEqual(len(jobs), 1)


if __name__ == '__main__':
    unittest.main()
