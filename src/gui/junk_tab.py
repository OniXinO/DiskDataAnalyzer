"""
GUI вкладка для детектора сміття
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading

from core.junk_detector import JunkDetector


class JunkTab(ttk.Frame):
    """Вкладка для виявлення сміттєвих файлів"""

    def __init__(self, parent):
        super().__init__(parent)
        self.detector = None
        self.selected_folder = None
        self.junk_result = None

        self._create_widgets()

    def _create_widgets(self):
        """Створити віджети"""
        # Вибір папки
        folder_frame = ttk.LabelFrame(self, text="Папка для сканування", padding=10)
        folder_frame.pack(fill=tk.X, padx=10, pady=5)

        self.folder_entry = ttk.Entry(folder_frame, width=50)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        ttk.Button(folder_frame, text="Вибрати...",
                  command=self._select_folder).pack(side=tk.LEFT)

        # Налаштування
        settings_frame = ttk.LabelFrame(self, text="Типи сміття для пошуку", padding=10)
        settings_frame.pack(fill=tk.X, padx=10, pady=5)

        # Чекбокси для типів сміття
        self.temp_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Тимчасові файли",
                       variable=self.temp_var).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)

        self.backup_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Backup файли",
                       variable=self.backup_var).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        self.old_backup_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Застарілі backup",
                       variable=self.old_backup_var).grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)

        self.duplicates_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Дублікати",
                       variable=self.duplicates_var).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)

        self.empty_folders_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Порожні папки",
                       variable=self.empty_folders_var).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

        # Рекурсивно
        self.recursive_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Рекурсивно",
                       variable=self.recursive_var).grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)

        # Кнопка сканування
        self.scan_btn = ttk.Button(settings_frame, text="Сканувати",
                                   command=self._start_scan)
        self.scan_btn.grid(row=0, column=3, rowspan=2, padx=10)

        # Прогрес
        progress_frame = ttk.Frame(self)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)

        self.progress_var = tk.StringVar(value="Готово до роботи")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack(side=tk.LEFT)

        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # Результати
        results_frame = ttk.LabelFrame(self, text="Знайдене сміття", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Таблиця результатів
        columns = ("Файл", "Тип", "Розмір")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)

        self.results_tree.heading("Файл", text="Файл")
        self.results_tree.heading("Тип", text="Тип")
        self.results_tree.heading("Розмір", text="Розмір")

        self.results_tree.column("Файл", width=400)
        self.results_tree.column("Тип", width=150)
        self.results_tree.column("Розмір", width=100)

        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)

        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Кнопки дій
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=tk.X, padx=10, pady=5)

        self.delete_btn = ttk.Button(action_frame, text="Безпечне видалення",
                                     command=self._safe_delete, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        ttk.Label(action_frame, text="⚠️ Видалення незворотнє! Перевірте список перед видаленням.",
                 foreground="red").pack(side=tk.LEFT, padx=10)

        # Статистика
        self.stats_var = tk.StringVar(value="")
        ttk.Label(action_frame, textvariable=self.stats_var).pack(side=tk.RIGHT, padx=10)

    def _select_folder(self):
        """Вибрати папку"""
        folder = filedialog.askdirectory(title="Виберіть папку для сканування")
        if folder:
            self.selected_folder = folder
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

    def _start_scan(self):
        """Почати сканування"""
        if not self.selected_folder or not os.path.exists(self.selected_folder):
            messagebox.showerror("Помилка", "Виберіть існуючу папку")
            return

        # Очистити результати
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Запустити в окремому потоці
        self.scan_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.progress_var.set("Сканування...")

        thread = threading.Thread(target=self._scan_junk, daemon=True)
        thread.start()

    def _scan_junk(self):
        """Сканувати сміття (в окремому потоці)"""
        try:
            # Створити детектор
            self.detector = JunkDetector(
                self.selected_folder,
                recursive=self.recursive_var.get()
            )

            # Виявити сміття
            self.junk_result = self.detector.detect()

            # Оновити GUI в головному потоці
            self.after(0, self._update_results)

        except Exception as e:
            self.after(0, self._show_error, str(e))

    def _update_results(self):
        """Оновити таблицю результатів"""
        if not self.junk_result:
            return

        # Додати результати згідно з вибраними типами
        if self.temp_var.get():
            for file in self.junk_result['temp_files']:
                size = self._get_file_size(file)
                rel_path = os.path.relpath(file, self.selected_folder)
                self.results_tree.insert('', tk.END, values=(rel_path, "Тимчасовий", size))

        if self.backup_var.get():
            for file in self.junk_result['backup_files']:
                size = self._get_file_size(file)
                rel_path = os.path.relpath(file, self.selected_folder)
                self.results_tree.insert('', tk.END, values=(rel_path, "Backup", size))

        if self.old_backup_var.get():
            for file in self.junk_result['old_backups']:
                size = self._get_file_size(file)
                rel_path = os.path.relpath(file, self.selected_folder)
                self.results_tree.insert('', tk.END, values=(rel_path, "Застарілий backup", size))

        if self.duplicates_var.get():
            for group in self.junk_result['duplicates']:
                # Показати всі дублікати крім першого
                for file in group[1:]:
                    size = self._get_file_size(file)
                    rel_path = os.path.relpath(file, self.selected_folder)
                    self.results_tree.insert('', tk.END, values=(rel_path, "Дублікат", size))

        if self.empty_folders_var.get():
            for folder in self.junk_result['empty_folders']:
                rel_path = os.path.relpath(folder, self.selected_folder)
                self.results_tree.insert('', tk.END, values=(rel_path, "Порожня папка", "0 B"))

        # Оновити статистику
        if self.detector:
            stats = self.detector.get_stats()
            total_size = self._format_size(stats['total_junk_size'])
            self.stats_var.set(f"Знайдено: {stats['total_junk_files']} файлів | Розмір: {total_size}")

        # Увімкнути кнопку видалення
        if self.results_tree.get_children():
            self.delete_btn.config(state=tk.NORMAL)

        self.progress_bar.stop()
        self.progress_var.set("Готово")
        self.scan_btn.config(state=tk.NORMAL)

    def _get_file_size(self, file_path: str) -> str:
        """Отримати розмір файлу"""
        try:
            size = os.path.getsize(file_path)
            return self._format_size(size)
        except OSError:
            return "0 B"

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
        self.scan_btn.config(state=tk.NORMAL)
        messagebox.showerror("Помилка сканування", error)

    def _safe_delete(self):
        """Безпечне видалення вибраних файлів"""
        if not self.results_tree.get_children():
            messagebox.showwarning("Попередження", "Немає файлів для видалення")
            return

        # Підтвердження
        count = len(self.results_tree.get_children())
        response = messagebox.askyesno(
            "Підтвердження видалення",
            f"Ви впевнені що хочете видалити {count} файлів/папок?\n\n"
            "⚠️ Ця операція незворотня!"
        )

        if not response:
            return

        # Видалити файли
        deleted_count = 0
        errors = []

        for item in self.results_tree.get_children():
            values = self.results_tree.item(item)['values']
            rel_path = values[0]
            full_path = os.path.join(self.selected_folder, rel_path)

            try:
                if os.path.isfile(full_path):
                    os.remove(full_path)
                    deleted_count += 1
                elif os.path.isdir(full_path):
                    os.rmdir(full_path)
                    deleted_count += 1
            except Exception as e:
                errors.append(f"{rel_path}: {str(e)}")

        # Показати результат
        if errors:
            error_msg = "\n".join(errors[:10])
            if len(errors) > 10:
                error_msg += f"\n... та ще {len(errors) - 10} помилок"

            messagebox.showwarning(
                "Видалення завершено з помилками",
                f"Видалено: {deleted_count}\nПомилки: {len(errors)}\n\n{error_msg}"
            )
        else:
            messagebox.showinfo("Успіх", f"Успішно видалено {deleted_count} файлів/папок")

        # Очистити результати
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        self.delete_btn.config(state=tk.DISABLED)
        self.stats_var.set("")
