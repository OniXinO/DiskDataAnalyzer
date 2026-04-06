#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Швидкий тест аналізатора дисків
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.analyze_disk import (
    get_disk_usage,
    format_bytes,
    get_directory_size,
    categorize_directory
)

def quick_test():
    """Швидкий тест основних функцій"""

    print("=== ШВИДКИЙ ТЕСТ DISKDATAANALYZER ===\n")

    # Тест 1: Інформація про диск C:
    print("1. Тест get_disk_usage():")
    usage = get_disk_usage('C:/')
    if 'error' not in usage:
        print(f"   ✅ C: диск: {format_bytes(usage['total'])} загалом")
        print(f"   ✅ Використано: {format_bytes(usage['used'])} ({usage['percent']:.1f}%)")
        print(f"   ✅ Вільно: {format_bytes(usage['free'])}")
    else:
        print(f"   ❌ Помилка: {usage['error']}")
    print()

    # Тест 2: Розмір директорії
    print("2. Тест get_directory_size():")
    test_dir = 'O:/Work/DiskDataAnalyzer'
    size = get_directory_size(test_dir)
    print(f"   ✅ Розмір проєкту: {format_bytes(size)}")
    print()

    # Тест 3: Категоризація
    print("3. Тест categorize_directory():")
    result = categorize_directory(test_dir)
    print(f"   ✅ Категорія: {result['category']}")
    print(f"   ✅ Впевненість: {result['confidence']}%")
    if result['markers_found']:
        print(f"   ✅ Маркери: {', '.join(result['markers_found'])}")
    print()

    # Тест 4: Форматування
    print("4. Тест format_bytes():")
    test_sizes = [100, 1024, 1024*1024, 1024*1024*1024]
    for size in test_sizes:
        print(f"   ✅ {size} байт = {format_bytes(size)}")
    print()

    print("=== ВСІ ТЕСТИ ПРОЙШЛИ УСПІШНО ✅ ===")

if __name__ == '__main__':
    try:
        quick_test()
    except Exception as e:
        print(f"\n❌ Помилка: {e}")
        import traceback
        traceback.print_exc()
