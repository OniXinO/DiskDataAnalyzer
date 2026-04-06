"""
Вкладка вибору диску для аналізу
"""

import tkinter as tk
from tkinter import ttk
import string
import os


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
        # Буде реалізовано в наступній задачі
        pass
