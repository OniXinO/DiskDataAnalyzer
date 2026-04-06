"""
Побудова дерева каталогів
"""

import os
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class DirectoryTree:
    """Побудова дерева каталогів з фільтрацією"""

    # Патерни для ігнорування за замовчуванням
    DEFAULT_IGNORE_PATTERNS = [
        '.git',
        '.svn',
        '__pycache__',
        'node_modules',
        '.DS_Store',
        'Thumbs.db'
    ]

    def __init__(self, root_path: str,
                 ignore_patterns: Optional[List[str]] = None,
                 max_depth: Optional[int] = None):
        """
        Ініціалізувати побудовник дерева

        Args:
            root_path: Кореневий шлях для побудови дерева
            ignore_patterns: Список патернів для ігнорування (glob-style)
            max_depth: Максимальна глибина рекурсії (None = необмежено)
        """
        if not os.path.exists(root_path):
            raise FileNotFoundError(f"Path does not exist: {root_path}")

        self.root_path = os.path.abspath(root_path)
        self.ignore_patterns = ignore_patterns if ignore_patterns is not None else self.DEFAULT_IGNORE_PATTERNS
        self.max_depth = max_depth
        self.tree = None
        self.stats = {
            'total_files': 0,
            'total_directories': 0,
            'total_size': 0
        }

    def build(self) -> Dict[str, Any]:
        """
        Побудувати дерево каталогів

        Returns:
            Dict з деревом каталогів
        """
        # Скинути статистику
        self.stats = {
            'total_files': 0,
            'total_directories': 0,
            'total_size': 0
        }

        self.tree = self._build_tree(self.root_path, depth=0)
        return self.tree

    def _build_tree(self, path: str, depth: int) -> Dict[str, Any]:
        """
        Рекурсивно побудувати дерево

        Args:
            path: Поточний шлях
            depth: Поточна глибина

        Returns:
            Dict з вузлом дерева
        """
        name = os.path.basename(path) or path
        is_dir = os.path.isdir(path)

        node = {
            'name': name,
            'path': path,
            'type': 'directory' if is_dir else 'file'
        }

        if not is_dir:
            # Файл
            try:
                size = os.path.getsize(path)
                node['size'] = size
                self.stats['total_files'] += 1
                self.stats['total_size'] += size
            except OSError:
                node['size'] = 0

            return node

        # Каталог
        self.stats['total_directories'] += 1
        node['children'] = []

        # Перевірити глибину
        if self.max_depth is not None and depth >= self.max_depth:
            return node

        # Читати вміст каталогу
        try:
            entries = os.listdir(path)
        except PermissionError:
            logger.warning(f"Permission denied: {path}")
            return node

        # Фільтрувати та сортувати
        filtered_entries = []
        for entry in entries:
            if self._should_ignore(entry):
                continue
            filtered_entries.append(entry)

        filtered_entries.sort()

        # Рекурсивно обробити кожен запис
        for entry in filtered_entries:
            entry_path = os.path.join(path, entry)
            try:
                child_node = self._build_tree(entry_path, depth + 1)
                node['children'].append(child_node)
            except Exception as e:
                logger.error(f"Error processing {entry_path}: {e}")

        return node

    def _should_ignore(self, name: str) -> bool:
        """
        Перевірити чи потрібно ігнорувати файл/папку

        Args:
            name: Ім'я файлу/папки

        Returns:
            True якщо потрібно ігнорувати
        """
        for pattern in self.ignore_patterns:
            # Простий glob matching
            if pattern.endswith('*'):
                if name.startswith(pattern[:-1]):
                    return True
            elif pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return True
            else:
                if name == pattern or name.startswith(pattern):
                    return True

        return False

    def export_to_text(self, use_unicode: bool = True) -> str:
        """
        Експортувати дерево в текстовий формат

        Args:
            use_unicode: Використовувати Unicode символи для дерева

        Returns:
            Текстове представлення дерева
        """
        if self.tree is None:
            raise ValueError("Tree not built. Call build() first.")

        if use_unicode:
            symbols = {
                'branch': '├── ',
                'last': '└── ',
                'vertical': '│   ',
                'space': '    '
            }
        else:
            symbols = {
                'branch': '|-- ',
                'last': '`-- ',
                'vertical': '|   ',
                'space': '    '
            }

        lines = [self.tree['name']]
        self._export_node(self.tree, '', True, lines, symbols)

        return '\n'.join(lines)

    def _export_node(self, node: Dict[str, Any], prefix: str,
                    is_last: bool, lines: List[str],
                    symbols: Dict[str, str]):
        """
        Рекурсивно експортувати вузол

        Args:
            node: Вузол дерева
            prefix: Префікс для відступу
            is_last: Чи це останній елемент
            lines: Список рядків результату
            symbols: Символи для малювання дерева
        """
        if 'children' not in node:
            return

        children = node['children']
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)

            # Символ для поточного елемента
            symbol = symbols['last'] if is_last_child else symbols['branch']

            # Додати рядок
            lines.append(prefix + symbol + child['name'])

            # Рекурсивно обробити дітей
            if child['type'] == 'directory' and 'children' in child:
                # Префікс для дітей
                if is_last_child:
                    child_prefix = prefix + symbols['space']
                else:
                    child_prefix = prefix + symbols['vertical']

                self._export_node(child, child_prefix, is_last_child, lines, symbols)

    def get_stats(self) -> Dict[str, Any]:
        """
        Отримати статистику дерева

        Returns:
            Dict зі статистикою
        """
        if self.tree is None:
            raise ValueError("Tree not built. Call build() first.")

        return self.stats.copy()
