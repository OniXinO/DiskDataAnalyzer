"""
GUI вкладка для класифікації файлів
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from typing import Optional

from core.file_classifier import FileClassifier
from core.llm_registry import LLMRegistry


class ClassifierTab(ttk.Frame):
    """Вкладка для класифікації файлів через LLM"""

    def __init__(self, parent):
        super().__init__(parent)
        self.classifier = None
        self.selected_folder = None

        self._create_widgets()

    def _create_widgets(self):
        """Створити віджети"""
        # Вибір папки
        folder_frame = ttk.LabelFrame(self, text="Папка для класифікації", padding=10)
        folder_frame.pack(fill=tk.X, padx=10, pady=5)

        self.folder_entry = ttk.Entry(folder_frame, width=50)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        ttk.Button(folder_frame, text="Вибрати...",
                  command=self._select_folder).pack(side=tk.LEFT)

        # Налаштування
        settings_frame = ttk.LabelFrame(self, text="Налаштування", padding=10)
        settings_frame.pack(fill=tk.X, padx=10, pady=5)

        # LLM провайдер
        ttk.Label(settings_frame, text="LLM провайдер:").grid(row=0, column=0, sticky=tk.W, pady=5)

        self.provider_var = tk.StringVar(value="Без LLM")
        providers = ["Без LLM"] + LLMRegistry.list_providers()
        self.provider_combo = ttk.Combobox(settings_frame, textvariable=self.provider_var,
                                          values=providers, state="readonly", width=20)
        self.provider_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Рекурсивно
        self.recursive_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Рекурсивно",
                       variable=self.recursive_var).grid(row=0, column=2, padx=10)

        # Кнопка класифікації
        self.classify_btn = ttk.Button(settings_frame, text="Класифікувати",
                                       command=self._start_classification)
        self.classify_btn.grid(row=0, column=3, padx=5)

        # Прогрес
        progress_frame = ttk.Frame(self)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)

        self.progress_var = tk.StringVar(value="Готово до роботи")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack(side=tk.LEFT)

        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # Результати
        results_frame = ttk.LabelFrame(self, text="Результати класифікації", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Таблиця результатів
        columns = ("Файл", "Категорія", "Опис", "Метод", "Впевненість")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.results_tree.heading(col, text=col)
            if col == "Файл":
                self.results_tree.column(col, width=300)
            elif col == "Опис":
                self.results_tree.column(col, width=250)
            else:
                self.results_tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)

        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Кнопки експорту
        export_frame = ttk.Frame(self)
        export_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(export_frame, text="Експорт CSV",
                  command=self._export_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="Експорт JSON",
                  command=self._export_json).pack(side=tk.LEFT)

        # Статистика
        self.stats_var = tk.StringVar(value="")
        ttk.Label(export_frame, textvariable=self.stats_var).pack(side=tk.RIGHT, padx=10)

    def _select_folder(self):
        """Вибрати папку"""
        folder = filedialog.askdirectory(title="Виберіть папку для класифікації")
        if folder:
            self.selected_folder = folder
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

    def _start_classification(self):
        """Почати класифікацію"""
        if not self.selected_folder or not os.path.exists(self.selected_folder):
            messagebox.showerror("Помилка", "Виберіть існуючу папку")
            return

        # Очистити результати
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Запустити в окремому потоці
        self.classify_btn.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.progress_var.set("Класифікація...")

        thread = threading.Thread(target=self._classify_files, daemon=True)
        thread.start()

    def _classify_files(self):
        """Класифікувати файли (в окремому потоці)"""
        try:
            # Створити класифікатор
            use_llm = self.provider_var.get() != "Без LLM"
            llm_provider = None

            if use_llm:
                provider_name = self.provider_var.get()
                # TODO: Отримати API ключ від користувача
                # Поки що без LLM провайдера
                pass

            self.classifier = FileClassifier(llm_provider=llm_provider)

            # Отримати файли
            files = self._get_files(self.selected_folder, self.recursive_var.get())

            # Класифікувати кожен файл
            results = []
            for file_path in files:
                try:
                    size = os.path.getsize(file_path)
                    mtime = os.path.getmtime(file_path)
                    parent_dir = os.path.dirname(file_path)

                    result = self.classifier.classify(
                        os.path.basename(file_path),
                        size=size,
                        mtime=int(mtime),
                        parent_dir=parent_dir,
                        use_llm=use_llm
                    )

                    results.append({
                        'file': file_path,
                        'category': result.get('category', 'unknown'),
                        'description': result.get('description_uk', ''),
                        'method': result.get('method', 'unknown'),
                        'confidence': result.get('confidence', 0.0)
                    })

                except Exception as e:
                    print(f"Error classifying {file_path}: {e}")

            # Оновити GUI в головному потоці
            self.after(0, self._update_results, results)

        except Exception as e:
            self.after(0, self._show_error, str(e))

    def _get_files(self, folder: str, recursive: bool) -> list:
        """Отримати список файлів"""
        files = []

        if recursive:
            for root, dirs, filenames in os.walk(folder):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
        else:
            try:
                entries = os.listdir(folder)
                for entry in entries:
                    entry_path = os.path.join(folder, entry)
                    if os.path.isfile(entry_path):
                        files.append(entry_path)
            except PermissionError:
                pass

        return files

    def _update_results(self, results: list):
        """Оновити таблицю результатів"""
        for result in results:
            rel_path = os.path.relpath(result['file'], self.selected_folder)
            self.results_tree.insert('', tk.END, values=(
                rel_path,
                result['category'],
                result['description'],
                result['method'],
                f"{result['confidence']:.2f}"
            ))

        # Оновити статистику
        if self.classifier:
            stats = self.classifier.get_stats()
            self.stats_var.set(f"Класифіковано: {stats['total_classified']} файлів")

        self.progress_bar.stop()
        self.progress_var.set("Готово")
        self.classify_btn.config(state=tk.NORMAL)

    def _show_error(self, error: str):
        """Показати помилку"""
        self.progress_bar.stop()
        self.progress_var.set("Помилка")
        self.classify_btn.config(state=tk.NORMAL)
        messagebox.showerror("Помилка класифікації", error)

    def _export_csv(self):
        """Експортувати в CSV"""
        if not self.results_tree.get_children():
            messagebox.showwarning("Попередження", "Немає результатів для експорту")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filename:
            try:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Файл", "Категорія", "Опис", "Метод", "Впевненість"])

                    for item in self.results_tree.get_children():
                        values = self.results_tree.item(item)['values']
                        writer.writerow(values)

                messagebox.showinfo("Успіх", f"Експортовано в {filename}")
            except Exception as e:
                messagebox.showerror("Помилка", f"Помилка експорту: {e}")

    def _export_json(self):
        """Експортувати в JSON"""
        if not self.results_tree.get_children():
            messagebox.showwarning("Попередження", "Немає результатів для експорту")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                import json
                results = []

                for item in self.results_tree.get_children():
                    values = self.results_tree.item(item)['values']
                    results.append({
                        'file': values[0],
                        'category': values[1],
                        'description': values[2],
                        'method': values[3],
                        'confidence': float(values[4])
                    })

                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)

                messagebox.showinfo("Успіх", f"Експортовано в {filename}")
            except Exception as e:
                messagebox.showerror("Помилка", f"Помилка експорту: {e}")
