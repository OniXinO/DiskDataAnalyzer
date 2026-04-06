"""
Пошук великих файлів на диску
"""

import os
from typing import List, Dict


def find_large_files(directory: str, min_size: int = 100*1024*1024, limit: int = 10) -> List[Dict]:
    """
    Знайти найбільші файли в директорії

    Args:
        directory: Шлях до директорії для пошуку
        min_size: Мінімальний розмір файлу в байтах (за замовчуванням 100MB)
        limit: Максимальна кількість файлів для повернення

    Returns:
        List[Dict]: Список словників з інформацією про файли
                   [{'name': str, 'path': str, 'size': int}, ...]
                   Відсортовано за розміром (від більшого до меншого)
    """
    large_files = []

    try:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)

                try:
                    # Пропускаємо символічні посилання
                    if os.path.islink(filepath):
                        continue

                    file_size = os.path.getsize(filepath)

                    if file_size >= min_size:
                        large_files.append({
                            'name': filename,
                            'path': filepath,
                            'size': file_size
                        })

                except (OSError, PermissionError):
                    # Пропускаємо файли до яких немає доступу
                    continue

        # Сортуємо за розміром (від більшого до меншого)
        large_files.sort(key=lambda x: x['size'], reverse=True)

        # Обмежуємо кількість результатів
        return large_files[:limit]

    except Exception:
        return []
