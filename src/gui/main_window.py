"""
Головне GUI вікно DiskDataAnalyzer
"""

import tkinter as tk
from tkinter import ttk


class MainWindow:
    """Головне вікно програми"""

    def __init__(self, root):
        """
        Ініціалізація головного вікна

        Args:
            root: Tkinter root вікно
        """
        self.root = root
        self.title = "DiskDataAnalyzer"
        self.root.title(self.title)
        self.root.geometry("1000x700")

        self._create_widgets()

    def _create_widgets(self):
        """Створення віджетів"""
        # Notebook для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
