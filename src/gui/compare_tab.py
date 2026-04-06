"""
GUI вкладка для порівняння папок
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading

from core.folder_compare import FolderCompare


class CompareTab(ttk.Frame):
    """Вкладка для порівняння двох папок"""

    def __init__(self, parent):
        super().__init__(parent)
        self.comparer = None
        self.folder1 = None
        self.folder2 = None

        self._create_widgets()

    def _create_widgets(self):
        """Створити віджети"""
        # Вибір папок
        folders_frame = ttk.LabelFrame(self, text="Папки для порівняння", padding=10)
        folders_frame.pack(fill=tk.X, padx=10, pady=5)

        # Перша папка
        ttk.Label(folders_frame, text="Папка 1:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.folder1_entry = ttk.Entry(folders_frame, width=40)
        self.folder1_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        ttk.Button(folders_frame, text="Вибрати...",
                  command=lambda: self._select_folder(1)).grid(row=0, column=2, padx=5)

        # Друга папка
        ttk.Label(folders_frame, text="Папка 2:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.folder2_entry = ttk.Entry(folders_frame, width=40)
        self.folder2_entry.grid(row=1, column=1, sticky=tk.EW, padx=5)
        ttk.Button(folders_frame, text="Вибрати...",
                  command=lambda: self._select_folder(2)).grid(row=1, column=2, padx=5)

        folders_frame.grid_columnconfigure(1, weight=1)

        # Налаштування
        settings_frame = ttk.LabelFrame(self, text="Налаштування", padding=10)
        settings_frame.pack(fill=tk.X, padx=10, pady=5)

        # Рекурсивно
        self.recursive_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Рекурсивно",
                       variable=self.recursive_var).grid(row=0, column=0, padx=5)

        # Використовувати hash
        self.use_hash_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Порівняння за hash",
                       variable=self.use_hash_var).grid(row=0, column=1, padx=5)

        # Кнопка порівняння
        self.compare_btn = ttk.Button(settings_frame, text="Порівняти",
                                      command=self._start_comparison)
        self.compare_btn.grid(row=0, column=2, padx=10)

        # Прогрес
        progress_frame = ttk.Frame(self)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)

        self.progress_var = tk.StringVar(value="Готово до роботи")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack(side=tk.LEFT)

        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # Результати
        results_frame = ttk.LabelFrame(self, text="Результати порівняння", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Таблиця результатів
        columns = ("Файл", "Статус")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=20)

        self.results_tree.heading("Файл", text="Файл")
        self.results_tree.heading("Статус", text="Статус")

        self.results_tree.column("Файл", width=400)
        self.results_tree.column("Статус", width=200)

        # Кольорові теги
        self.results_tree.tag_configure('identical', foreground='green')
        self.results_tree.tag_configure('different', foreground='orange')
        self.results_tree.tag_configure('only_first', foreground='blue')
        self.results_tree.tag_configure('only_second', foreground='red')

        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)

        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Кнопки експорту
        export_frame = ttk.Frame(self)
        export_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(export_frame, text="Експорт звіт",
                  command=self._export_report).pack(side=tk.LEFT, padx=5)

        # Статистика
        self.stats_var = tk.StringVar(value="")
        ttk.Label(export_frame, textvariable=self.stats_var).pack(side=tk.RIGHT, padx=10)

    def _select_folder(self, folder_num: int):
        """Вибрати папку"""
        folder = filedialog.askdirectory(title=f"Виберіть папку {folder_num}")
        if folder:
            if folder_num == 1:
                self.folder1 = folder
                self.folder1_entry.delete(0, tk.END)
                self.folder1_entry.insert(0, folder)
            else:
                self.folder2 = folder
                self.folder2_entry.delete(0, tk.END)
                self.folder2_entry.insert(0, folder)

    def _start_comparison(self):
        """Почати порівняння"""
        if not self.folder1 or not os.path.exists(self.folder1):
            messagebox.showerror("Помилка", "Виберіть існуючу папку 1")
            return

        if not self.folder2 or not os.path.exists(self.folder2):
            messagebox.showerror("Помилка", "Виберіть існуючу папку 2")
            return

        # Очистити результати
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Запустити в окремому потоці
        self.compare_btn.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.progress_var.set("Порівняння...")

        thread = threading.Thread(target=self._compare_folders, daemon=True)
        thread.start()

    def _compare_folders(self):
        """Порівняти папки (в окремому потоці)"""
        try:
            # Створити компаратор
            self.comparer = FolderCompare(
                self.folder1,
                self.folder2,
                recursive=self.recursive_var.get(),
                use_hash=self.use_hash_var.get()
            )

            # Порівняти
            result = self.comparer.compare()

            # Оновити GUI в головному потоці
            self.after(0, self._update_results, result)

        except Exception as e:
            self.after(0, self._show_error, str(e))

    def _update_results(self, result: dict):
        """Оновити таблицю результатів"""
        # Ідентичні файли
        for file in result['identical']:
            self.results_tree.insert('', tk.END,
                                    values=(file, "✓ Ідентичні"),
                                    tags=('identical',))

        # Різні файли
        for file in result['different']:
            self.results_tree.insert('', tk.END,
                                    values=(file, "≠ Різний вміст"),
                                    tags=('different',))

        # Тільки в першій
        for file in result['only_in_first']:
            self.results_tree.insert('', tk.END,
                                    values=(file, "→ Тільки в папці 1"),
                                    tags=('only_first',))

        # Тільки в другій
        for file in result['only_in_second']:
            self.results_tree.insert('', tk.END,
                                    values=(file, "← Тільки в папці 2"),
                                    tags=('only_second',))

        # Оновити статистику
        if self.comparer:
            stats = self.comparer.get_stats()
            self.stats_var.set(
                f"Ідентичні: {stats['identical_count']} | "
                f"Різні: {stats['different_count']} | "
                f"Тільки в 1: {stats['only_in_first_count']} | "
                f"Тільки в 2: {stats['only_in_second_count']}"
            )

        self.progress_bar.stop()
        self.progress_var.set("Готово")
        self.compare_btn.config(state=tk.NORMAL)

    def _show_error(self, error: str):
        """Показати помилку"""
        self.progress_bar.stop()
        self.progress_var.set("Помилка")
        self.compare_btn.config(state=tk.NORMAL)
        messagebox.showerror("Помилка порівняння", error)

    def _export_report(self):
        """Експортувати звіт"""
        if not self.comparer:
            messagebox.showwarning("Попередження", "Спочатку виконайте порівняння")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if filename:
            try:
                report = self.comparer.get_report()

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)

                messagebox.showinfo("Успіх", f"Звіт експортовано в {filename}")
            except Exception as e:
                messagebox.showerror("Помилка", f"Помилка експорту: {e}")
