"""
Модуль для створення та порівняння знімків диску
"""

import json
from datetime import datetime
from core.analyze_disk import analyze_disk


def create_snapshot(drive, output_file):
    """
    Створити знімок стану диску

    Args:
        drive: Шлях до диску або директорії
        output_file: Шлях до файлу для збереження знімку

    Returns:
        dict: Створений знімок
    """
    # Аналізуємо диск
    results = analyze_disk(drive, report_dir=None)

    # Створюємо знімок
    snapshot = {
        'timestamp': datetime.now().isoformat(),
        'drive': drive,
        'usage': results.get('usage', {}),
        'top_directories': results.get('top_directories', []),
        'file_types': results.get('file_types', {})
    }

    # Зберігаємо в файл
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=2)

    return snapshot


def compare_snapshots(snapshot1, snapshot2):
    """
    Порівняти два знімки диску

    Args:
        snapshot1: Перший знімок (старіший)
        snapshot2: Другий знімок (новіший)

    Returns:
        dict: Різниця між знімками
    """
    diff = {
        'added': [],
        'removed': [],
        'modified': [],
        'size_change': 0
    }

    # Порівняння usage
    if 'usage' in snapshot1 and 'usage' in snapshot2:
        used1 = snapshot1['usage'].get('used', 0)
        used2 = snapshot2['usage'].get('used', 0)
        diff['size_change'] = used2 - used1

    # Порівняння директорій
    dirs1 = {d['path']: d['size'] for d in snapshot1.get('top_directories', [])}
    dirs2 = {d['path']: d['size'] for d in snapshot2.get('top_directories', [])}

    # Додані директорії
    diff['added'] = list(set(dirs2.keys()) - set(dirs1.keys()))

    # Видалені директорії
    diff['removed'] = list(set(dirs1.keys()) - set(dirs2.keys()))

    # Змінені директорії
    for path in set(dirs1.keys()) & set(dirs2.keys()):
        if dirs1[path] != dirs2[path]:
            diff['modified'].append({
                'path': path,
                'old_size': dirs1[path],
                'new_size': dirs2[path],
                'change': dirs2[path] - dirs1[path]
            })

    return diff
