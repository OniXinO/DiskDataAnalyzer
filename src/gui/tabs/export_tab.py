"""
Вкладка експорту результатів аналізу
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from exporters.json_exporter import export_to_json
from exporters.csv_exporter import export_to_csv
from exporters.html_exporter import export_to_html


class ExportTab(ttk.Frame):
    """Вкладка для експорту результатів"""

    def __init__(self, parent, results):
        """
        Ініціалізація вкладки

        Args:
            parent: Батьківський віджет
            results: Результати аналізу (словник)
        """
        super().__init__(parent)
        self.results = results
        self._create_widgets()

    def _create_widgets(self):
        """Створення віджетів вкладки"""
        if not self.results:
            ttk.Label(
                self,
                text="No results to export",
                font=('Arial', 12)
            ).pack(pady=20)
            return

        # Заголовок
        ttk.Label(self, text="Export Results:", font=('Arial', 12, 'bold')).pack(pady=10)

        # Frame для вибору формату
        format_frame = ttk.Frame(self)
        format_frame.pack(pady=10)

        ttk.Label(format_frame, text="Format:", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)

        # Radiobuttons для вибору формату
        self.format_var = tk.StringVar(value='JSON')
        formats = ['JSON', 'CSV', 'HTML']

        for fmt in formats:
            ttk.Radiobutton(
                format_frame,
                text=fmt,
                variable=self.format_var,
                value=fmt
            ).pack(side=tk.LEFT, padx=5)

        # Кнопка експорту
        self.export_btn = ttk.Button(
            self,
            text="Export",
            command=self.export_results
        )
        self.export_btn.pack(pady=10)

        # Статус лейбл
        self.status_label = ttk.Label(self, text="", font=('Arial', 10))
        self.status_label.pack(pady=5)

    def export_results(self):
        """Експортувати результати у вибраному форматі"""
        fmt = self.format_var.get()

        # Вибір файлу для збереження
        filetypes = {
            'JSON': [('JSON files', '*.json')],
            'CSV': [('CSV files', '*.csv')],
            'HTML': [('HTML files', '*.html')]
        }

        default_ext = {
            'JSON': '.json',
            'CSV': '.csv',
            'HTML': '.html'
        }

        filepath = filedialog.asksaveasfilename(
            defaultextension=default_ext[fmt],
            filetypes=filetypes[fmt]
        )

        if not filepath:
            return

        try:
            # Експорт у вибраному форматі
            if fmt == 'JSON':
                export_to_json(self.results, filepath)
            elif fmt == 'CSV':
                export_to_csv(self.results, filepath)
            elif fmt == 'HTML':
                export_to_html(self.results, filepath)

            self.status_label.config(
                text=f'Exported to {os.path.basename(filepath)}',
                foreground='green'
            )
            messagebox.showinfo('Success', f'Results exported to {filepath}')
        except Exception as e:
            self.status_label.config(
                text=f'Error: {str(e)}',
                foreground='red'
            )
            messagebox.showerror('Error', f'Failed to export: {str(e)}')
