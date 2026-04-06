"""
Гібридний класифікатор файлів
90% класифікація за patterns/extensions, 10% через LLM
"""

import os
import logging
from typing import Dict, Any, Optional
from core.classification_cache import ClassificationCache

logger = logging.getLogger(__name__)


class FileClassifier:
    """Гібридний класифікатор файлів з кешуванням"""

    # Класифікація за розширеннями
    EXTENSION_MAP = {
        # Інсталятори
        'exe': 'installer',
        'msi': 'installer',
        'dmg': 'installer',
        'pkg': 'installer',
        'deb': 'installer',
        'rpm': 'installer',
        'apk': 'installer',

        # Документи
        'doc': 'document',
        'docx': 'document',
        'pdf': 'document',
        'txt': 'document',
        'rtf': 'document',
        'odt': 'document',
        'xls': 'document',
        'xlsx': 'document',
        'ppt': 'document',
        'pptx': 'document',

        # Зображення
        'jpg': 'image',
        'jpeg': 'image',
        'png': 'image',
        'gif': 'image',
        'bmp': 'image',
        'svg': 'image',
        'webp': 'image',
        'ico': 'image',

        # Відео
        'mp4': 'video',
        'avi': 'video',
        'mkv': 'video',
        'mov': 'video',
        'wmv': 'video',
        'flv': 'video',
        'webm': 'video',

        # Аудіо
        'mp3': 'audio',
        'wav': 'audio',
        'flac': 'audio',
        'aac': 'audio',
        'ogg': 'audio',
        'wma': 'audio',

        # Архіви
        'zip': 'archive',
        'rar': 'archive',
        '7z': 'archive',
        'tar': 'archive',
        'gz': 'archive',
        'bz2': 'archive',
        'xz': 'archive',

        # Код
        'py': 'code',
        'js': 'code',
        'java': 'code',
        'cpp': 'code',
        'c': 'code',
        'h': 'code',
        'cs': 'code',
        'php': 'code',
        'rb': 'code',
        'go': 'code',
        'rs': 'code',

        # Конфігурація
        'json': 'config',
        'xml': 'config',
        'yaml': 'config',
        'yml': 'config',
        'ini': 'config',
        'conf': 'config',
        'cfg': 'config',

        # Дані
        'db': 'data',
        'sqlite': 'data',
        'sql': 'data',
        'csv': 'data',

        # Системні
        'dll': 'system',
        'sys': 'system',
        'so': 'system',
        'dylib': 'system',

        # Тимчасові
        'tmp': 'temp',
        'temp': 'temp',
        'cache': 'temp',
    }

    # Патерни в назві файлу
    PATTERN_MAP = {
        'installer': ['install', 'setup', 'installer'],
        'backup': ['backup', 'bak', '.bak'],
        'temp': ['temp', 'tmp', 'cache'],
        'log': ['log', '.log'],
        'config': ['config', 'settings', 'preferences'],
    }

    # Описи категорій українською
    CATEGORY_DESCRIPTIONS = {
        'installer': 'Інсталятор програми',
        'document': 'Документ',
        'image': 'Зображення',
        'video': 'Відео файл',
        'audio': 'Аудіо файл',
        'archive': 'Архів',
        'code': 'Програмний код',
        'config': 'Конфігураційний файл',
        'data': 'Файл даних',
        'system': 'Системний файл',
        'temp': 'Тимчасовий файл',
        'backup': 'Резервна копія',
        'log': 'Лог файл',
        'other': 'Інший файл',
    }

    def __init__(self, cache_db: str = "classification_cache.db",
                 llm_provider=None):
        """
        Ініціалізувати класифікатор

        Args:
            cache_db: Шлях до SQLite бази для кешу
            llm_provider: LLM провайдер для складних випадків (опціонально)
        """
        self.cache = ClassificationCache(cache_db)
        self.llm_provider = llm_provider
        self.stats = {
            'total_classified': 0,
            'by_method': {},
            'by_category': {}
        }

    def classify(self, filename: str, size: int, mtime: int,
                parent_dir: str = "", use_llm: bool = True) -> Dict[str, Any]:
        """
        Класифікувати файл

        Args:
            filename: Ім'я файлу
            size: Розмір в байтах
            mtime: Час модифікації (timestamp)
            parent_dir: Батьківська папка (опціонально)
            use_llm: Чи використовувати LLM для невідомих файлів

        Returns:
            Dict з результатом класифікації
        """
        # Перевірити кеш
        cached = self.cache.get(filename, size, mtime)
        if cached:
            result = cached.copy()
            result['from_cache'] = True
            self._update_stats(result['category'], 'cache')
            return result

        # Спробувати класифікувати за розширенням
        result = self._classify_by_extension(filename)
        if result:
            result['method'] = 'extension'
            self._cache_and_return(filename, size, mtime, result)
            return result

        # Спробувати класифікувати за патерном
        result = self._classify_by_pattern(filename)
        if result:
            result['method'] = 'pattern'
            self._cache_and_return(filename, size, mtime, result)
            return result

        # Якщо дозволено, спробувати LLM
        if use_llm and self.llm_provider:
            result = self._classify_by_llm(filename, size, parent_dir)
            if result:
                result['method'] = 'llm'
                self._cache_and_return(filename, size, mtime, result)
                return result

        # Fallback - невідома категорія
        result = {
            'category': 'other',
            'description_uk': 'Невідомий тип файлу',
            'confidence': 0.3,
            'method': 'fallback',
            'from_cache': False
        }
        self._cache_and_return(filename, size, mtime, result)
        return result

    def _classify_by_extension(self, filename: str) -> Optional[Dict[str, Any]]:
        """Класифікувати за розширенням"""
        ext = os.path.splitext(filename)[1].lower().lstrip('.')

        if ext in self.EXTENSION_MAP:
            category = self.EXTENSION_MAP[ext]
            return {
                'category': category,
                'description_uk': self.CATEGORY_DESCRIPTIONS.get(category, 'Файл'),
                'confidence': 0.9,
                'from_cache': False
            }

        return None

    def _classify_by_pattern(self, filename: str) -> Optional[Dict[str, Any]]:
        """Класифікувати за патерном в назві"""
        filename_lower = filename.lower()

        for category, patterns in self.PATTERN_MAP.items():
            for pattern in patterns:
                if pattern in filename_lower:
                    return {
                        'category': category,
                        'description_uk': self.CATEGORY_DESCRIPTIONS.get(category, 'Файл'),
                        'confidence': 0.85,
                        'from_cache': False
                    }

        return None

    def _classify_by_llm(self, filename: str, size: int,
                        parent_dir: str) -> Optional[Dict[str, Any]]:
        """Класифікувати через LLM провайдер"""
        if not self.llm_provider:
            return None

        try:
            context = {
                'size': size,
                'extension': os.path.splitext(filename)[1],
                'parent_dir': parent_dir
            }

            result = self.llm_provider.classify_file(filename, context)
            result['from_cache'] = False
            return result

        except Exception as e:
            logger.error(f"LLM classification error: {e}")
            return None

    def _cache_and_return(self, filename: str, size: int, mtime: int,
                         result: Dict[str, Any]) -> Dict[str, Any]:
        """Зберегти в кеш та оновити статистику"""
        # Зберегти в кеш
        self.cache.set(filename, size, mtime,
                      provider=result.get('method', 'unknown'),
                      result=result)

        # Оновити статистику
        self._update_stats(result['category'], result.get('method', 'unknown'))

        return result

    def _update_stats(self, category: str, method: str):
        """Оновити статистику класифікації"""
        self.stats['total_classified'] += 1

        if method not in self.stats['by_method']:
            self.stats['by_method'][method] = 0
        self.stats['by_method'][method] += 1

        if category not in self.stats['by_category']:
            self.stats['by_category'][category] = 0
        self.stats['by_category'][category] += 1

    def get_stats(self) -> Dict[str, Any]:
        """Отримати статистику класифікації"""
        return self.stats.copy()
