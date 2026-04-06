"""
JSON експортер для звітів аналізу диску
"""

import json
from typing import Any, Dict


def export_to_json(data: Dict[str, Any], output_file: str) -> None:
    """
    Експортувати дані у JSON файл

    Args:
        data: Словник з даними для експорту
        output_file: Шлях до вихідного JSON файлу

    Returns:
        None
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,  # Підтримка Unicode
            indent=2             # Pretty print з відступами
        )
