"""
Головне GUI вікно DiskDataAnalyzer
"""

import tkinter as tk
from tkinter import ttk

from gui.classifier_tab import ClassifierTab
from gui.tree_tab import TreeTab
from gui.compare_tab import CompareTab
from gui.junk_tab import JunkTab


class MainWindow:
    """Головне вікно програми"""

    def __init__(self, root):
        """
        Ініціалізація головного вікна

        Args:
            root: Tkinter root вікно
        """
        self.root = root
        self.title = "DiskDataAnalyzer v0.5.0"
        self.root.title(self.title)
        self.root.geometry("1000x700")

        self._create_widgets()

    def _create_widgets(self):
        """Створення віджетів"""
        # Notebook для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Нові вкладки Phase 5
        self.classifier_tab = ClassifierTab(self.notebook)
        self.notebook.add(self.classifier_tab, text="File Classifier")

        self.tree_tab = TreeTab(self.notebook)
        self.notebook.add(self.tree_tab, text="Directory Tree")

        self.compare_tab = CompareTab(self.notebook)
        self.notebook.add(self.compare_tab, text="Folder Compare")

        self.junk_tab = JunkTab(self.notebook)
        self.notebook.add(self.junk_tab, text="Junk Detector")
