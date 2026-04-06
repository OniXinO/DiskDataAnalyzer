"""
CSV експортер для звітів аналізу диску
"""

import csv
from typing import List, Dict, Any


def export_to_csv(data: List[Dict[str, Any]], output_file: str) -> None:
    """
    Експортувати дані у CSV файл

    Args:
        data: Список словників з даними для експорту
        output_file: Шлях до вихідного CSV файлу

    Returns:
        None
    """
    if not data:
        # Створюємо порожній файл для порожнього списку
        with open(output_file, 'w', encoding='utf-8') as f:
            pass
        return

    # Отримуємо заголовки з першого елемента
    fieldnames = list(data[0].keys())

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
