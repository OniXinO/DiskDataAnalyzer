"""
Тести для worker потоку аналізу
"""

import unittest
import threading
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gui.workers.analysis_worker import AnalysisWorker


class TestAnalysisWorker(unittest.TestCase):
    """Тести для AnalysisWorker"""

    def test_worker_is_thread(self):
        """Тест що worker є потоком"""
        results = []
        worker = AnalysisWorker("C:", callback=lambda x: results.append(x))
        self.assertIsInstance(worker, threading.Thread)

    def test_worker_runs_in_background(self):
        """Тест що worker запускається в окремому потоці"""
        results = []
        worker = AnalysisWorker("C:", callback=lambda x: results.append(x))
        worker.start()

        # Worker має бути живим після старту
        self.assertTrue(worker.is_alive())

        # Чекаємо завершення (з timeout)
        worker.join(timeout=5)

    def test_worker_calls_callback(self):
        """Тест що worker викликає callback з результатами"""
        import tempfile
        results = []

        def callback(data):
            results.append(data)

        # Використовуємо тимчасову директорію замість реального диску
        test_dir = tempfile.mkdtemp()
        worker = AnalysisWorker(test_dir, callback=callback)
        worker.start()
        worker.join(timeout=10)

        # Callback має бути викликаний
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], dict)

        # Cleanup
        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)

    def test_worker_is_daemon(self):
        """Тест що worker є daemon потоком"""
        worker = AnalysisWorker("C:", callback=lambda x: None)
        self.assertTrue(worker.daemon)


if __name__ == '__main__':
    unittest.main()
