"""
DiskDataAnalyzer - Main Entry Point
Запуск GUI додатку
"""

import tkinter as tk
from gui.main_window import MainWindow


def main():
    """Головна функція запуску додатку"""
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
