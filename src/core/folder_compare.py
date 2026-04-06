"""
Порівняння папок
"""

import os
import hashlib
import logging
from typing import Dict, Any, List, Set

logger = logging.getLogger(__name__)


class FolderCompare:
    """Порівняння двох папок за структурою та вмістом"""

    def __init__(self, path1: str, path2: str,
                 recursive: bool = True,
                 use_hash: bool = True):
        """
        Ініціалізувати компаратор папок

        Args:
            path1: Перша папка для порівняння
            path2: Друга папка для порівняння
            recursive: Рекурсивне порівняння підпапок
            use_hash: Використовувати hash для порівняння вмісту файлів
        """
        if not os.path.exists(path1):
            raise FileNotFoundError(f"Path does not exist: {path1}")
        if not os.path.exists(path2):
            raise FileNotFoundError(f"Path does not exist: {path2}")

        self.path1 = os.path.abspath(path1)
        self.path2 = os.path.abspath(path2)
        self.recursive = recursive
        self.use_hash = use_hash

        self.result = None

    def compare(self) -> Dict[str, List[str]]:
        """
        Порівняти дві папки

        Returns:
            Dict з результатами порівняння:
            - identical: список ідентичних файлів
            - different: список файлів з різним вмістом
            - only_in_first: файли тільки в першій папці
            - only_in_second: файли тільки в другій папці
        """
        # Отримати списки файлів
        files1 = self._get_files(self.path1)
        files2 = self._get_files(self.path2)

        # Отримати відносні шляхи
        rel_files1 = {self._get_relative_path(f, self.path1): f for f in files1}
        rel_files2 = {self._get_relative_path(f, self.path2): f for f in files2}

        # Знайти спільні та унікальні файли
        common_files = set(rel_files1.keys()) & set(rel_files2.keys())
        only_in_first = set(rel_files1.keys()) - set(rel_files2.keys())
        only_in_second = set(rel_files2.keys()) - set(rel_files1.keys())

        # Порівняти спільні файли
        identical = []
        different = []

        for rel_path in common_files:
            file1 = rel_files1[rel_path]
            file2 = rel_files2[rel_path]

            if self._files_identical(file1, file2):
                identical.append(rel_path)
            else:
                different.append(rel_path)

        self.result = {
            'identical': sorted(identical),
            'different': sorted(different),
            'only_in_first': sorted(list(only_in_first)),
            'only_in_second': sorted(list(only_in_second))
        }

        return self.result

    def _get_files(self, path: str) -> List[str]:
        """
        Отримати список файлів в папці

        Args:
            path: Шлях до папки

        Returns:
            Список абсолютних шляхів до файлів
        """
        files = []

        if self.recursive:
            for root, dirs, filenames in os.walk(path):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
        else:
            try:
                entries = os.listdir(path)
                for entry in entries:
                    entry_path = os.path.join(path, entry)
                    if os.path.isfile(entry_path):
                        files.append(entry_path)
            except PermissionError:
                logger.warning(f"Permission denied: {path}")

        return files

    def _get_relative_path(self, file_path: str, base_path: str) -> str:
        """
        Отримати відносний шлях файлу

        Args:
            file_path: Абсолютний шлях до файлу
            base_path: Базовий шлях

        Returns:
            Відносний шлях
        """
        return os.path.relpath(file_path, base_path)

    def _files_identical(self, file1: str, file2: str) -> bool:
        """
        Перевірити чи файли ідентичні

        Args:
            file1: Шлях до першого файлу
            file2: Шлях до другого файлу

        Returns:
            True якщо файли ідентичні
        """
        if self.use_hash:
            return self._compare_by_hash(file1, file2)
        else:
            return self._compare_by_size_and_mtime(file1, file2)

    def _compare_by_hash(self, file1: str, file2: str) -> bool:
        """
        Порівняти файли за hash

        Args:
            file1: Шлях до першого файлу
            file2: Шлях до другого файлу

        Returns:
            True якщо hash однакові
        """
        try:
            hash1 = self._calculate_hash(file1)
            hash2 = self._calculate_hash(file2)
            return hash1 == hash2
        except Exception as e:
            logger.error(f"Error comparing files by hash: {e}")
            return False

    def _calculate_hash(self, file_path: str, algorithm: str = 'md5') -> str:
        """
        Обчислити hash файлу

        Args:
            file_path: Шлях до файлу
            algorithm: Алгоритм hash (md5, sha256)

        Returns:
            Hash файлу
        """
        hash_obj = hashlib.new(algorithm)

        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_obj.update(chunk)

        return hash_obj.hexdigest()

    def _compare_by_size_and_mtime(self, file1: str, file2: str) -> bool:
        """
        Порівняти файли за розміром та часом модифікації

        Args:
            file1: Шлях до першого файлу
            file2: Шлях до другого файлу

        Returns:
            True якщо розмір та mtime однакові
        """
        try:
            stat1 = os.stat(file1)
            stat2 = os.stat(file2)

            return (stat1.st_size == stat2.st_size and
                   abs(stat1.st_mtime - stat2.st_mtime) < 1)
        except Exception as e:
            logger.error(f"Error comparing files by size/mtime: {e}")
            return False

    def get_report(self) -> str:
        """
        Отримати текстовий звіт про порівняння

        Returns:
            Текстовий звіт
        """
        if self.result is None:
            raise ValueError("Comparison not performed. Call compare() first.")

        lines = []
        lines.append("=" * 60)
        lines.append("FOLDER COMPARISON REPORT")
        lines.append("=" * 60)
        lines.append(f"Path 1: {self.path1}")
        lines.append(f"Path 2: {self.path2}")
        lines.append("")

        # Статистика
        stats = self.get_stats()
        lines.append("STATISTICS:")
        lines.append(f"  Identical files: {stats['identical_count']}")
        lines.append(f"  Different files: {stats['different_count']}")
        lines.append(f"  Only in first:   {stats['only_in_first_count']}")
        lines.append(f"  Only in second:  {stats['only_in_second_count']}")
        lines.append("")

        # Деталі
        if self.result['identical']:
            lines.append("IDENTICAL FILES:")
            for file in self.result['identical'][:10]:  # Перші 10
                lines.append(f"  ✓ {file}")
            if len(self.result['identical']) > 10:
                lines.append(f"  ... and {len(self.result['identical']) - 10} more")
            lines.append("")

        if self.result['different']:
            lines.append("DIFFERENT FILES:")
            for file in self.result['different']:
                lines.append(f"  ≠ {file}")
            lines.append("")

        if self.result['only_in_first']:
            lines.append("ONLY IN FIRST:")
            for file in self.result['only_in_first']:
                lines.append(f"  → {file}")
            lines.append("")

        if self.result['only_in_second']:
            lines.append("ONLY IN SECOND:")
            for file in self.result['only_in_second']:
                lines.append(f"  ← {file}")
            lines.append("")

        lines.append("=" * 60)

        return '\n'.join(lines)

    def get_stats(self) -> Dict[str, int]:
        """
        Отримати статистику порівняння

        Returns:
            Dict зі статистикою
        """
        if self.result is None:
            raise ValueError("Comparison not performed. Call compare() first.")

        return {
            'identical_count': len(self.result['identical']),
            'different_count': len(self.result['different']),
            'only_in_first_count': len(self.result['only_in_first']),
            'only_in_second_count': len(self.result['only_in_second'])
        }
