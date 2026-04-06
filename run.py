#!/usr/bin/env python3
"""
DiskDataAnalyzer - Application Entry Point

Зручний entry point для запуску GUI додатку з кореня проєкту.
"""

import sys
import tkinter as tk
from src.gui.main_window import MainWindow


def main():
    """Головна функція запуску додатку"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
