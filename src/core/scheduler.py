"""
Планувальник для періодичного аналізу диску
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from core.analyze_disk import analyze_disk


class DiskScheduler:
    """Планувальник для автоматичного аналізу диску"""

    def __init__(self):
        """Ініціалізація планувальника"""
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def schedule_analysis(self, drive, interval_hours, report_dir):
        """
        Запланувати періодичний аналіз диску

        Args:
            drive: Літера диску (наприклад 'C:')
            interval_hours: Інтервал в годинах
            report_dir: Директорія для звітів

        Returns:
            Job: Створений job
        """
        job = self.scheduler.add_job(
            func=analyze_disk,
            trigger=IntervalTrigger(hours=interval_hours),
            args=[drive, report_dir],
            id=f'analysis_{drive}',
            replace_existing=True
        )
        return job

    def remove_job(self, drive):
        """
        Видалити заплановану задачу

        Args:
            drive: Літера диску
        """
        self.scheduler.remove_job(f'analysis_{drive}')

    def list_jobs(self):
        """
        Отримати список всіх запланованих задач

        Returns:
            list: Список jobs
        """
        return self.scheduler.get_jobs()

    def shutdown(self):
        """Зупинити планувальник"""
        self.scheduler.shutdown()
