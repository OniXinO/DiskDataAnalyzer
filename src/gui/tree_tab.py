"""
GUI вкладка для дерева каталогів
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading

from core.directory_tree import DirectoryTree


class TreeTab(ttk.Frame):
    """Вкладка для візуалізації дерева каталогів"""

    def __init__(self, parent):
        super().__init__(parent)
        self.tree_builder = None
        self.selected_folder = None
        self.tree_data = None

        self._create_widgets()

    def _create_widgets(self):
        """Створити віджети"""
        # Вибір папки
        folder_frame = ttk.LabelFrame(self, text="Папка для аналізу", padding=10)
        folder_frame.pack(fill=tk.X, padx=10, pady=5)

        self.folder_entry = ttk.Entry(folder_frame, width=50)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        ttk.Button(folder_frame, text="Вибрати...",
                  command=self._select_folder).pack(side=tk.LEFT)

        # Налаштування
        settings_frame = ttk.LabelFrame(self, text="Налаштування", padding=10)
        settings_frame.pack(fill=tk.X, padx=10, pady=5)

        # Фільтри
        ttk.Label(settings_frame, text="Ігнорувати:").grid(row=0, column=0, sticky=tk.W, pady=5)

        self.ignore_entry = ttk.Entry(settings_frame, width=30)
        self.ignore_entry.insert(0, ".git, __pycache__, node_modules")
        self.ignore_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Максимальна глибина
        ttk.Label(settings_frame, text="Макс. глибина:").grid(row=0, column=2, sticky=tk.W, padx=(10, 5))

        self.depth_var = tk.StringVar(value="Необмежено")
        depth_combo = ttk.Combobox(settings_frame, textvariable=self.depth_var,
                                   values=["Необмежено", "1", "2", "3", "5", "10"],
                                   state="readonly", width=12)
        depth_combo.grid(row=0, column=3, sticky=tk.W, padx=5)

        # Кнопка побудови
        self.build_btn = ttk.Button(settings_frame, text="Побудувати дерево",
                                    command=self._start_build)
        self.build_btn.grid(row=0, column=4, padx=10)

        # Прогрес
        progress_frame = ttk.Frame(self)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)

        self.progress_var = tk.StringVar(value="Готово до роботи")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack(side=tk.LEFT)

        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # Дерево
        tree_frame = ttk.LabelFrame(self, text="Структура каталогів", padding=10)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # TreeView для дерева
        self.tree_view = ttk.Treeview(tree_frame, height=20)
        self.tree_view.heading('#0', text='Структура папок та файлів')

        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_view.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree_view.xview)
        self.tree_view.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree_view.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=1, column=0, sticky=(tk.E, tk.W))

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Кнопки експорту
        export_frame = ttk.Frame(self)
        export_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(export_frame, text="Експорт текст",
                  command=self._export_text).pack(side=tk.LEFT, padx=5)

        # Статистика
        self.stats_var = tk.StringVar(value="")
        ttk.Label(export_frame, textvariable=self.stats_var).pack(side=tk.RIGHT, padx=10)

    def _select_folder(self):
        """Вибрати папку"""
        folder = filedialog.askdirectory(title="Виберіть папку для аналізу")
        if folder:
            self.selected_folder = folder
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

    def _start_build(self):
        """Почати побудову дерева"""
        if not self.selected_folder or not os.path.exists(self.selected_folder):
            messagebox.showerror("Помилка", "Виберіть існуючу папку")
            return

        # Очистити дерево
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        # Запустити в окремому потоці
        self.build_btn.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.progress_var.set("Побудова дерева...")

        thread = threading.Thread(target=self._build_tree, daemon=True)
        thread.start()

    def _build_tree(self):
        """Побудувати дерево (в окремому потоці)"""
        try:
            # Отримати параметри
            ignore_patterns = [p.strip() for p in self.ignore_entry.get().split(',') if p.strip()]

            max_depth = None
            if self.depth_var.get() != "Необмежено":
                max_depth = int(self.depth_var.get())

            # Побудувати дерево
            self.tree_builder = DirectoryTree(
                self.selected_folder,
                ignore_patterns=ignore_patterns,
                max_depth=max_depth
            )

            self.tree_data = self.tree_builder.build()

            # Оновити GUI в головному потоці
            self.after(0, self._update_tree_view)

        except Exception as e:
            self.after(0, self._show_error, str(e))

    def _update_tree_view(self):
        """Оновити TreeView"""
        if self.tree_data:
            # Додати кореневий вузол
            root_id = self.tree_view.insert('', tk.END, text=self.tree_data['name'], open=True)

            # Рекурсивно додати дітей
            if 'children' in self.tree_data:
                self._add_children(root_id, self.tree_data['children'])

        # Оновити статистику
        if self.tree_builder:
            stats = self.tree_builder.get_stats()
            self.stats_var.set(
                f"Файлів: {stats['total_files']} | "
                f"Папок: {stats['total_directories']} | "
                f"Розмір: {self._format_size(stats['total_size'])}"
            )

        self.progress_bar.stop()
        self.progress_var.set("Готово")
        self.build_btn.config(state=tk.NORMAL)

    def _add_children(self, parent_id: str, children: list):
        """Рекурсивно додати дітей до дерева"""
        for child in children:
            # Іконка для файлів/папок
            if child['type'] == 'directory':
                text = f"📁 {child['name']}"
            else:
                size_str = self._format_size(child.get('size', 0))
                text = f"📄 {child['name']} ({size_str})"

            child_id = self.tree_view.insert(parent_id, tk.END, text=text)

            # Рекурсивно додати дітей
            if 'children' in child and child['children']:
                self._add_children(child_id, child['children'])

    def _format_size(self, size: int) -> str:
        """Форматувати розмір"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def _show_error(self, error: str):
        """Показати помилку"""
        self.progress_bar.stop()
        self.progress_var.set("Помилка")
        self.build_btn.config(state=tk.NORMAL)
        messagebox.showerror("Помилка побудови дерева", error)

    def _export_text(self):
        """Експортувати в текстовий формат"""
        if not self.tree_builder or not self.tree_data:
            messagebox.showwarning("Попередження", "Спочатку побудуйте дерево")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if filename:
            try:
                text = self.tree_builder.export_to_text()

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)

                messagebox.showinfo("Успіх", f"Експортовано в {filename}")
            except Exception as e:
                messagebox.showerror("Помилка", f"Помилка експорту: {e}")
