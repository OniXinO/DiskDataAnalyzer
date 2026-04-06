"""
Вкладка вибору диску для аналізу
"""

import tkinter as tk
from tkinter import ttk
import string
import os
from gui.workers.analysis_worker import AnalysisWorker


class DriveTab(ttk.Frame):
    """Вкладка для вибору диску та запуску аналізу"""

    def __init__(self, parent):
        """
        Ініціалізація вкладки

        Args:
            parent: Батьківський віджет
        """
        super().__init__(parent)
        self._create_widgets()

    def _create_widgets(self):
        """Створення віджетів вкладки"""
        # Заголовок
        ttk.Label(self, text="Select Drive:", font=('Arial', 12, 'bold')).pack(pady=10)

        # Combobox для вибору диску
        self.drive_var = tk.StringVar()
        self.drive_combo = ttk.Combobox(
            self,
            textvariable=self.drive_var,
            state='readonly',
            width=30
        )
        self.drive_combo['values'] = self.get_available_drives()
        if self.drive_combo['values']:
            self.drive_combo.current(0)
        self.drive_combo.pack(pady=5)

        # Кнопка аналізу
        self.analyze_btn = ttk.Button(
            self,
            text="Analyze",
            command=self.start_analysis
        )
        self.analyze_btn.pack(pady=10)

        # Статус лейбл
        self.status_label = ttk.Label(self, text="", font=('Arial', 10))
        self.status_label.pack(pady=5)

    def get_available_drives(self):
        """
        Отримати список доступних дисків

        Returns:
            list: Список літер дисків (наприклад ['C:', 'D:'])
        """
        drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:"
            if os.path.exists(f"{drive}/"):
                drives.append(drive)
        return drives

    def start_analysis(self):
        """Запустити аналіз вибраного диску"""
        drive = self.drive_var.get()
        if not drive:
            self.status_label.config(text="Please select a drive", foreground='red')
            return

        # Блокуємо кнопку під час аналізу
        self.analyze_btn.config(state='disabled', text='Analyzing...')
        self.status_label.config(text=f'Analyzing {drive}...', foreground='blue')

        # Запускаємо worker в окремому потоці
        worker = AnalysisWorker(drive, self.on_analysis_complete)
        worker.start()

    def on_analysis_complete(self, results):
        """
        Callback після завершення аналізу

        Args:
            results: Результати аналізу
        """
        # Розблоковуємо кнопку
        self.analyze_btn.config(state='normal', text='Analyze')

        if 'error' in results:
            self.status_label.config(text=f"Error: {results['error']}", foreground='red')
        else:
            self.status_label.config(text='Analysis complete!', foreground='green')
            # Результати будуть відображені в наступній задачі

