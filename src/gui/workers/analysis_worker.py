"""
Worker потік для аналізу диску в фоновому режимі
"""

import threading
from core.analyze_disk import analyze_disk


class AnalysisWorker(threading.Thread):
    """Worker потік для запуску аналізу без блокування GUI"""

    def __init__(self, drive, callback):
        """
        Ініціалізація worker потоку

        Args:
            drive: Літера диску для аналізу (наприклад 'C:')
            callback: Функція для виклику з результатами
        """
        super().__init__()
        self.drive = drive
        self.callback = callback
        self.daemon = True  # Daemon потік завершиться разом з головною програмою

    def run(self):
        """Виконання аналізу в окремому потоці"""
        try:
            # Запускаємо аналіз без збереження звіту
            results = analyze_disk(self.drive, report_dir=None)
            self.callback(results)
        except Exception as e:
            # Повертаємо помилку через callback
            self.callback({'error': str(e)})
