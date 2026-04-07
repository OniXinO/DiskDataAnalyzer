"""
Розширений детектор сміттєвих файлів
"""

import os
import hashlib
import logging
import fnmatch
from typing import Dict, Any, List, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class JunkDetector:
    """Детектор сміттєвих файлів з розширеними можливостями"""

    # Розширення тимчасових файлів
    TEMP_EXTENSIONS = ['.tmp', '.temp', '.cache', '.bak~', '.swp', '.swo']

    # Розширення backup файлів
    BACKUP_EXTENSIONS = ['.bak', '.backup', '.old', '.orig', '~']

    # Системні файли за замовчуванням (не видаляти)
    DEFAULT_SYSTEM_WHITELIST = [
        'System32*',
        'Windows*',
        'Program Files*',
        '*.sys',
        '*.dll',
        'boot*',
        'ntldr',
        'bootmgr'
    ]

    def __init__(self, root_path: str,
                 recursive: bool = True,
                 old_backup_days: int = 90,
                 system_whitelist: Optional[List[str]] = None):
        """
        Ініціалізувати детектор сміття

        Args:
            root_path: Кореневий шлях для сканування
            recursive: Рекурсивне сканування
            old_backup_days: Кількість днів для визначення застарілих backup
            system_whitelist: Список патернів системних файлів (glob-style)
        """
        self.root_path = os.path.abspath(root_path)
        self.recursive = recursive
        self.old_backup_days = old_backup_days
        self.system_whitelist = system_whitelist or self.DEFAULT_SYSTEM_WHITELIST

        self.result = None

    def detect(self) -> Dict[str, Any]:
        """
        Виявити сміттєві файли

        Returns:
            Dict з категоріями сміття
        """
        self.result = {
            'temp_files': [],
            'backup_files': [],
            'old_backups': [],
            'duplicates': [],
            'empty_folders': []
        }

        # Отримати всі файли
        all_files = self._get_all_files()

        # Виявити різні типи сміття
        for file_path in all_files:
            # Пропустити файли з whitelist
            if self._is_whitelisted(file_path):
                continue

            # Тимчасові файли
            if self._is_temp_file(file_path):
                self.result['temp_files'].append(file_path)

            # Backup файли
            if self._is_backup_file(file_path):
                self.result['backup_files'].append(file_path)

                # Перевірити чи backup застарілий
                if self._is_old_backup(file_path):
                    self.result['old_backups'].append(file_path)

        # Виявити дублікати
        self.result['duplicates'] = self._find_duplicates(all_files)

        # Виявити порожні папки
        self.result['empty_folders'] = self._find_empty_folders()

        return self.result

    def _get_all_files(self) -> List[str]:
        """Отримати список всіх файлів"""
        files = []

        if self.recursive:
            for root, _, filenames in os.walk(self.root_path):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
        else:
            try:
                entries = os.listdir(self.root_path)
                for entry in entries:
                    entry_path = os.path.join(self.root_path, entry)
                    if os.path.isfile(entry_path):
                        files.append(entry_path)
            except PermissionError:
                logger.warning(f"Permission denied: {self.root_path}")

        return files

    def _is_whitelisted(self, file_path: str) -> bool:
        """Перевірити чи файл в whitelist"""
        filename = os.path.basename(file_path)

        for pattern in self.system_whitelist:
            if fnmatch.fnmatch(filename, pattern):
                return True

        return False

    def _is_temp_file(self, file_path: str) -> bool:
        """Перевірити чи файл тимчасовий"""
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.TEMP_EXTENSIONS

    def _is_backup_file(self, file_path: str) -> bool:
        """Перевірити чи файл backup"""
        filename = os.path.basename(file_path)

        # Перевірити розширення
        ext = os.path.splitext(file_path)[1].lower()
        if ext in self.BACKUP_EXTENSIONS:
            return True

        # Перевірити назву
        if 'backup' in filename.lower() or filename.endswith('~'):
            return True

        return False

    def _is_old_backup(self, file_path: str) -> bool:
        """Перевірити чи backup застарілий"""
        try:
            mtime = os.path.getmtime(file_path)
            age_days = (os.path.getctime(file_path) - mtime) / (24 * 60 * 60)

            # Використовуємо поточний час
            import time
            current_time = time.time()
            age_days = (current_time - mtime) / (24 * 60 * 60)

            return age_days > self.old_backup_days
        except OSError:
            return False

    def _find_duplicates(self, files: List[str]) -> List[List[str]]:
        """
        Знайти дублікати за hash

        Args:
            files: Список файлів для перевірки

        Returns:
            Список груп дублікатів
        """
        # Групувати файли за hash
        hash_groups = defaultdict(list)

        for file_path in files:
            # Пропустити файли з whitelist
            if self._is_whitelisted(file_path):
                continue

            try:
                file_hash = self._calculate_hash(file_path)
                hash_groups[file_hash].append(file_path)
            except Exception as e:
                logger.error(f"Error hashing {file_path}: {e}")

        # Повернути тільки групи з більш ніж 1 файлом
        duplicates = [group for group in hash_groups.values() if len(group) > 1]

        return duplicates

    def _calculate_hash(self, file_path: str, algorithm: str = 'md5') -> str:
        """Обчислити hash файлу"""
        hash_obj = hashlib.new(algorithm)

        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_obj.update(chunk)

        return hash_obj.hexdigest()

    def _find_empty_folders(self) -> List[str]:
        """Знайти порожні папки"""
        empty_folders = []

        if self.recursive:
            for root, _, _ in os.walk(self.root_path, topdown=False):
                # Пропустити кореневу папку
                if root == self.root_path:
                    continue

                # Перевірити чи папка порожня
                try:
                    if not os.listdir(root):
                        empty_folders.append(root)
                except PermissionError:
                    logger.warning(f"Permission denied: {root}")
        else:
            # Не-рекурсивний режим - перевірити тільки прямі підпапки
            try:
                entries = os.listdir(self.root_path)
                for entry in entries:
                    entry_path = os.path.join(self.root_path, entry)
                    if os.path.isdir(entry_path):
                        try:
                            if not os.listdir(entry_path):
                                empty_folders.append(entry_path)
                        except PermissionError:
                            pass
            except PermissionError:
                logger.warning(f"Permission denied: {self.root_path}")

        return empty_folders

    def is_safe_to_delete(self, file_path: str) -> bool:
        """
        Перевірити чи безпечно видаляти файл

        Args:
            file_path: Шлях до файлу

        Returns:
            True якщо безпечно видаляти
        """
        # Перевірити whitelist
        if self._is_whitelisted(file_path):
            return False

        # Якщо detect() не викликано, перевірити за правилами
        if self.result is None:
            # Безпечно видаляти тимчасові та backup файли
            return self._is_temp_file(file_path) or self._is_backup_file(file_path)

        # Перевірити чи файл в будь-якій категорії сміття
        for category, items in self.result.items():
            if category == 'duplicates':
                # duplicates - список груп
                for group in items:
                    if file_path in group:
                        return True
            elif isinstance(items, list):
                if file_path in items:
                    return True

        return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Отримати статистику сміття

        Returns:
            Dict зі статистикою
        """
        if self.result is None:
            raise ValueError("Detection not performed. Call detect() first.")

        total_files = 0
        total_size = 0
        by_category = {}

        for category, items in self.result.items():
            if category == 'duplicates':
                # Для дублікатів рахуємо всі файли крім одного в кожній групі
                dup_count = sum(len(group) - 1 for group in items)
                dup_size = 0
                for group in items:
                    # Розмір дублікатів = розмір всіх крім одного
                    if group:
                        try:
                            file_size = os.path.getsize(group[0])
                            dup_size += file_size * (len(group) - 1)
                        except OSError:
                            pass

                by_category[category] = {'count': dup_count, 'size': dup_size}
                total_files += dup_count
                total_size += dup_size

            elif category == 'empty_folders':
                by_category[category] = {'count': len(items), 'size': 0}

            else:
                # Звичайні файли
                cat_size = 0
                for file_path in items:
                    try:
                        cat_size += os.path.getsize(file_path)
                    except OSError:
                        pass

                by_category[category] = {'count': len(items), 'size': cat_size}
                total_files += len(items)
                total_size += cat_size

        return {
            'total_junk_files': total_files,
            'total_junk_size': total_size,
            'by_category': by_category
        }
