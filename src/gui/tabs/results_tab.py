"""
Вкладка відображення результатів аналізу з візуалізацією
"""

import tkinter as tk
from tkinter import ttk

try:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class ResultsTab(ttk.Frame):
    """Вкладка для відображення результатів аналізу"""

    def __init__(self, parent, results):
        """
        Ініціалізація вкладки

        Args:
            parent: Батьківський віджет
            results: Результати аналізу (словник)
        """
        super().__init__(parent)
        self.results = results
        self.figure = None
        self.canvas = None
        self._create_widgets()

    def _create_widgets(self):
        """Створення віджетів вкладки"""
        if not MATPLOTLIB_AVAILABLE:
            ttk.Label(
                self,
                text="Matplotlib not installed. Install with: pip install matplotlib",
                foreground='red'
            ).pack(pady=20)
            return

        if not self.results or 'usage' not in self.results:
            ttk.Label(
                self,
                text="No results to display",
                font=('Arial', 12)
            ).pack(pady=20)
            return

        # Створюємо matplotlib figure
        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Малюємо діаграму
        self._draw_usage_chart()

    def _draw_usage_chart(self):
        """Малювання pie chart використання диску"""
        if 'usage' not in self.results:
            return

        usage = self.results['usage']
        ax = self.figure.add_subplot(111)

        # Дані для pie chart
        sizes = [usage.get('used', 0), usage.get('free', 0)]
        labels = ['Used', 'Free']
        colors = ['#ff6b6b', '#51cf66']
        explode = (0.05, 0)  # Трохи виділяємо "Used"

        # Створюємо pie chart
        ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            explode=explode,
            shadow=True
        )

        ax.set_title('Disk Usage', fontsize=14, fontweight='bold')
        ax.axis('equal')  # Рівні пропорції для круглої діаграми

        self.canvas.draw()
