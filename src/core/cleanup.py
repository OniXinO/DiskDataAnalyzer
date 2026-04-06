"""
Модуль для очищення диску від дублікатів
"""

import os
from send2trash import send2trash


def select_files_for_deletion(duplicates, selected_indices):
    """
    Фільтрує файли для видалення на основі вибору користувача

    Args:
        duplicates: Список груп дублікатів
        selected_indices: Словник {group_index: [file_indices]}

    Returns:
        list: Відфільтрований список груп з вибраними файлами
    """
    result = []

    for group_idx, indices in selected_indices.items():
        if group_idx < len(duplicates):
            group = duplicates[group_idx]
            selected_files = [group['files'][i] for i in indices if i < len(group['files'])]

            if selected_files:
                result.append({'files': selected_files})

    return result


def cleanup_duplicates(duplicates, keep_first=True, dry_run=False):
    """
    Безпечно видаляє дублікати файлів переміщенням в корзину

    Args:
        duplicates: Список груп дублікатів [{'files': [path1, path2, ...]}, ...]
        keep_first: Зберегти перший файл в кожній групі
        dry_run: Не видаляти насправді, тільки показати що буде видалено

    Returns:
        dict: Статистика {'deleted': int, 'space_freed': int, 'errors': list}
    """
    stats = {
        'deleted': 0,
        'space_freed': 0,
        'errors': []
    }

    for group in duplicates:
        files = group.get('files', [])
        if len(files) < 2:
            continue

        # Визначаємо які файли видаляти
        to_delete = files[1:] if keep_first else files[:-1]

        for filepath in to_delete:
            try:
                if not dry_run:
                    # Отримуємо розмір перед видаленням
                    if os.path.exists(filepath):
                        size = os.path.getsize(filepath)
                        send2trash(filepath)
                        stats['deleted'] += 1
                        stats['space_freed'] += size
            except Exception as e:
                stats['errors'].append({
                    'file': filepath,
                    'error': str(e)
                })

    return stats
