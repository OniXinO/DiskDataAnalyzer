#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Універсальний скрипт аналізу дисків для Windows
Використання: python analyze_disk.py C: [--report-dir O:/disk_reports]
"""

import os
import sys
import argparse
from pathlib import Path
import shutil
from datetime import datetime
from collections import defaultdict
import hashlib
import zipfile
import tarfile
import json

# Імпорт експортерів
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from exporters.json_exporter import export_to_json
from exporters.csv_exporter import export_to_csv
from exporters.html_exporter import export_to_html

# Виправлення кодування для Windows консолі
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def get_disk_usage(path):
    """Отримати інформацію про використання диску"""
    try:
        total, used, free = shutil.disk_usage(path)
        return {
            'total': total,
            'used': used,
            'free': free,
            'percent': (used / total) * 100
        }
    except Exception as e:
        return {'error': str(e)}

def get_directory_size(path):
    """Отримати розмір директорії"""
    total = 0
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
                elif entry.is_dir(follow_symlinks=False):
                    # Перевірка на symlink перед рекурсією
                    if not entry.is_symlink():
                        total += get_directory_size(entry.path)
            except (PermissionError, FileNotFoundError, OSError):
                # Ігноруємо помилки доступу та циклічні посилання
                pass
    except (PermissionError, FileNotFoundError, OSError):
        pass
    return total

def format_bytes(bytes):
    """Форматувати байти в читабельний вигляд"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"

def calculate_file_hash(filepath, algorithm='md5'):
    """Обчислити хеш файлу"""
    hash_func = hashlib.md5() if algorithm == 'md5' else hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except (PermissionError, FileNotFoundError, OSError):
        return None

def analyze_archive(filepath):
    """Аналіз архіву (zip, tar, tar.gz, rar)"""
    result = {
        'type': None,
        'files_count': 0,
        'uncompressed_size': 0,
        'compression_ratio': 0,
        'file_list': []
    }

    try:
        if zipfile.is_zipfile(filepath):
            result['type'] = 'zip'
            with zipfile.ZipFile(filepath, 'r') as zf:
                for info in zf.infolist():
                    if not info.is_dir():
                        result['files_count'] += 1
                        result['uncompressed_size'] += info.file_size
                        result['file_list'].append({
                            'name': info.filename,
                            'size': info.file_size,
                            'compressed': info.compress_size
                        })
        elif tarfile.is_tarfile(filepath):
            result['type'] = 'tar'
            with tarfile.open(filepath, 'r:*') as tf:
                for member in tf.getmembers():
                    if member.isfile():
                        result['files_count'] += 1
                        result['uncompressed_size'] += member.size
                        result['file_list'].append({
                            'name': member.name,
                            'size': member.size
                        })
        else:
            # Try RAR
            try:
                import rarfile
                if rarfile.is_rarfile(filepath):
                    result['type'] = 'rar'
                    with rarfile.RarFile(filepath, 'r') as rf:
                        for info in rf.infolist():
                            if not info.isdir():
                                result['files_count'] += 1
                                result['uncompressed_size'] += info.file_size
                                result['file_list'].append({
                                    'name': info.filename,
                                    'size': info.file_size,
                                    'compressed': info.compress_size
                                })
            except ImportError:
                pass  # rarfile not installed

            # Try 7z
            if result['type'] is None and filepath.endswith('.7z'):
                try:
                    import py7zr
                    with py7zr.SevenZipFile(filepath, 'r') as zf:
                        result['type'] = '7z'
                        for name, info in zf.list():
                            if not info.is_directory:
                                result['files_count'] += 1
                                result['uncompressed_size'] += info.uncompressed
                                result['file_list'].append({
                                    'name': name,
                                    'size': info.uncompressed
                                })
                except ImportError:
                    pass  # py7zr not installed
                except Exception:
                    pass  # Invalid 7z file

        if result['uncompressed_size'] > 0:
            compressed_size = os.path.getsize(filepath)
            result['compression_ratio'] = (1 - compressed_size / result['uncompressed_size']) * 100

    except Exception as e:
        result['error'] = str(e)

    return result

def categorize_directory(dir_path):
    """Визначити категорію та призначення директорії"""
    dir_name = os.path.basename(dir_path).lower()

    # Маркери для різних категорій
    categories = {
        'project': {
            'markers': ['.git', '.gitignore', 'package.json', 'requirements.txt',
                       'pom.xml', 'build.gradle', 'Cargo.toml', 'go.mod'],
            'keywords': ['project', 'dev', 'code', 'src', 'repo']
        },
        'backup': {
            'markers': [],
            'keywords': ['backup', 'bak', 'old', 'archive', 'copy']
        },
        'media': {
            'markers': [],
            'keywords': ['photo', 'video', 'music', 'media', 'pictures', 'movies']
        },
        'game': {
            'markers': [],
            'keywords': ['game', 'steam', 'epic', 'gog']
        },
        'document': {
            'markers': [],
            'keywords': ['doc', 'document', 'paper', 'report', 'work']
        },
        'system': {
            'markers': [],
            'keywords': ['windows', 'program files', 'programdata', 'appdata', 'system']
        }
    }

    result = {
        'category': 'unknown',
        'confidence': 0,
        'markers_found': [],
        'file_types': defaultdict(int),
        'is_active': False
    }

    # Перевірка маркерів
    try:
        entries = list(os.scandir(dir_path))

        for category, data in categories.items():
            for marker in data['markers']:
                if any(marker in entry.name for entry in entries):
                    result['markers_found'].append(marker)
                    result['category'] = category
                    result['confidence'] = 80
                    break

        # Перевірка за ключовими словами
        if result['confidence'] < 50:
            for category, data in categories.items():
                if any(keyword in dir_name for keyword in data['keywords']):
                    result['category'] = category
                    result['confidence'] = 60
                    break

        # Аналіз типів файлів
        for entry in entries[:100]:  # Обмежуємо для швидкості
            if entry.is_file():
                ext = Path(entry.name).suffix.lower()
                result['file_types'][ext] += 1

        # Визначення активності (файли змінювались останні 30 днів)
        recent_threshold = datetime.now().timestamp() - (30 * 24 * 60 * 60)
        for entry in entries[:50]:
            if entry.is_file() and entry.stat().st_mtime > recent_threshold:
                result['is_active'] = True
                break

    except (PermissionError, FileNotFoundError):
        pass

    return result

def find_duplicates(path, min_size=1024*1024):
    """Знайти дублікати файлів (за хешем)"""
    size_map = defaultdict(list)
    hash_map = defaultdict(list)

    print(f"🔍 Пошук дублікатів (мін. розмір: {format_bytes(min_size)})...")

    # Групування за розміром
    try:
        for root, dirs, files in os.walk(path):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    size = os.path.getsize(filepath)
                    if size >= min_size:
                        size_map[size].append(filepath)
                except (PermissionError, FileNotFoundError, OSError):
                    pass
    except (PermissionError, FileNotFoundError):
        pass

    # Обчислення хешів для файлів однакового розміру
    duplicates = []
    for size, files in size_map.items():
        if len(files) > 1:
            for filepath in files:
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    hash_map[file_hash].append(filepath)

    # Збір дублікатів
    for file_hash, files in hash_map.items():
        if len(files) > 1:
            size = os.path.getsize(files[0])
            duplicates.append({
                'hash': file_hash,
                'size': size,
                'count': len(files),
                'files': files,
                'wasted_space': size * (len(files) - 1)
            })

    # Сортування за втраченим місцем
    duplicates.sort(key=lambda x: x['wasted_space'], reverse=True)

    return duplicates

def get_file_types_distribution(path, max_depth=2):
    """Отримати розподіл файлів за типами"""
    extensions = defaultdict(lambda: {'count': 0, 'size': 0})

    def scan_directory(dir_path, current_depth=0):
        if current_depth > max_depth:
            return
        try:
            for entry in os.scandir(dir_path):
                if entry.is_file(follow_symlinks=False):
                    ext = Path(entry.name).suffix.lower() or '.no_extension'
                    size = entry.stat().st_size
                    extensions[ext]['count'] += 1
                    extensions[ext]['size'] += size
                elif entry.is_dir(follow_symlinks=False):
                    scan_directory(entry.path, current_depth + 1)
        except (PermissionError, FileNotFoundError):
            pass

    scan_directory(path)
    return extensions

def analyze_disk(drive_letter, report_dir='O:/disk_reports'):
    """Аналіз диску"""
    drive_path = f'{drive_letter}/'
    drive_name = drive_letter.rstrip(':')

    print(f"=== АНАЛІЗ ДИСКУ {drive_letter} ===\n")

    # Перевірка існування диску
    if not os.path.exists(drive_path):
        print(f"❌ Диск {drive_letter} не знайдено або недоступний")
        return None

    results = {
        'drive': drive_letter,
        'timestamp': datetime.now().isoformat(),
        'usage': {},
        'top_directories': [],
        'temp_files': [],
        'file_types': {},
        'archives': [],
        'categories': {},
        'duplicates': []
    }

    # 1. Загальна інформація
    print("📊 Загальна інформація...")
    usage = get_disk_usage(drive_path)
    if 'error' not in usage:
        results['usage'] = usage
        print(f"Загальний розмір: {format_bytes(usage['total'])}")
        print(f"Використано: {format_bytes(usage['used'])} ({usage['percent']:.1f}%)")
        print(f"Вільно: {format_bytes(usage['free'])}")
        print()

    # 2. Топ-20 найбільших директорій
    print("📁 Сканування найбільших директорій...")

    # Список типових директорій для сканування
    common_dirs = [
        'Windows', 'Program Files', 'Program Files (x86)', 'Users',
        'ProgramData', 'Temp', 'Work', 'Projects', 'Documents',
        'Downloads', 'Desktop', 'AppData', 'Games', 'Steam'
    ]

    sizes = []
    for dir_name in common_dirs:
        dir_path = os.path.join(drive_path, dir_name)
        if os.path.exists(dir_path):
            print(f"  Сканування {dir_path}...")
            size = get_directory_size(dir_path)
            sizes.append((dir_path, size))

    # Сортування за розміром
    sizes.sort(key=lambda x: x[1], reverse=True)
    results['top_directories'] = sizes[:20]

    print("\n📊 Топ-20 найбільших директорій:")
    for path, size in sizes[:20]:
        print(f"{format_bytes(size):>12} - {path}")

    # 3. Тимчасові файли
    print("\n🗑️ Тимчасові файли...")
    temp_dirs = []

    if drive_name == 'C':
        temp_dirs = [
            'C:/Windows/Temp',
            os.path.join(str(Path.home()), 'AppData/Local/Temp'),
            'C:/Temp',
        ]
    else:
        temp_dirs = [
            f'{drive_letter}/Temp',
            f'{drive_letter}/tmp',
        ]

    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            size = get_directory_size(temp_dir)
            results['temp_files'].append({'path': temp_dir, 'size': size})
            print(f"{format_bytes(size):>12} - {temp_dir}")

    # 4. Розподіл файлів за типами (тільки для невеликих дисків)
    if usage.get('used', 0) < 500 * 1024 * 1024 * 1024:  # < 500GB
        print("\n📄 Аналіз типів файлів (це може зайняти час)...")
        file_types = get_file_types_distribution(drive_path, max_depth=2)

        # Топ-10 типів за розміром
        sorted_types = sorted(file_types.items(), key=lambda x: x[1]['size'], reverse=True)[:10]
        results['file_types'] = dict(sorted_types)

        print("\n📊 Топ-10 типів файлів за розміром:")
        for ext, data in sorted_types:
            print(f"{format_bytes(data['size']):>12} - {ext} ({data['count']} файлів)")

    # 5. Аналіз архівів
    print("\n📦 Пошук та аналіз архівів...")
    archive_extensions = ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz']
    archives_found = []

    for dir_path, size in sizes[:10]:  # Тільки в топ-10 директоріях
        try:
            for entry in os.scandir(dir_path):
                if entry.is_file() and Path(entry.name).suffix.lower() in archive_extensions:
                    archive_info = analyze_archive(entry.path)
                    if archive_info['type']:
                        archives_found.append({
                            'path': entry.path,
                            'size': entry.stat().st_size,
                            **archive_info
                        })
        except (PermissionError, FileNotFoundError):
            pass

    results['archives'] = sorted(archives_found, key=lambda x: x['size'], reverse=True)[:20]

    if archives_found:
        print(f"\nЗнайдено архівів: {len(archives_found)}")
        print("\n📦 Топ-10 найбільших архівів:")
        for archive in results['archives'][:10]:
            ratio = archive.get('compression_ratio', 0)
            print(f"{format_bytes(archive['size']):>12} - {archive['path']}")
            print(f"             ({archive['files_count']} файлів, "
                  f"стиснення: {ratio:.1f}%)")

    # 6. Категоризація директорій
    print("\n🏷️ Категоризація директорій...")
    categories_stats = defaultdict(lambda: {'count': 0, 'size': 0, 'active': 0})

    for dir_path, size in sizes[:20]:
        category_info = categorize_directory(dir_path)
        category = category_info['category']

        categories_stats[category]['count'] += 1
        categories_stats[category]['size'] += size
        if category_info['is_active']:
            categories_stats[category]['active'] += 1

        results['categories'][dir_path] = category_info

    print("\n🏷️ Розподіл за категоріями:")
    for category, stats in sorted(categories_stats.items(), key=lambda x: x[1]['size'], reverse=True):
        print(f"{category:12} - {stats['count']} директорій, "
              f"{format_bytes(stats['size'])}, активних: {stats['active']}")

    # 7. Пошук дублікатів (опціонально, тільки для невеликих дисків)
    if usage.get('used', 0) < 100 * 1024 * 1024 * 1024:  # < 100GB
        print("\n🔍 Пошук дублікатів...")
        duplicates = find_duplicates(drive_path, min_size=10*1024*1024)  # мін 10MB

        results['duplicates'] = duplicates[:20]

        if duplicates:
            total_wasted = sum(d['wasted_space'] for d in duplicates)
            print(f"\nЗнайдено груп дублікатів: {len(duplicates)}")
            print(f"Втрачено місця: {format_bytes(total_wasted)}")

            print("\n🔍 Топ-5 груп дублікатів:")
            for dup in duplicates[:5]:
                print(f"{format_bytes(dup['wasted_space']):>12} - "
                      f"{dup['count']} копій файлу ({format_bytes(dup['size'])})")
                for filepath in dup['files'][:3]:
                    print(f"             {filepath}")

    # 8. Генерація звіту
    if report_dir:
        print(f"\n💾 Генерація звіту...")
        generate_report(results, report_dir)

    return results

def generate_report(results, report_dir):
    """Генерація markdown звіту"""
    os.makedirs(report_dir, exist_ok=True)

    drive_name = results['drive'].rstrip(':')
    report_path = os.path.join(report_dir, f'{drive_name}_drive_analysis.md')

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# Аналіз диску {results['drive']}\n\n")
        f.write(f"**Дата аналізу:** {results['timestamp']}\n\n")

        # Загальна інформація
        if results['usage']:
            usage = results['usage']
            f.write("## 📊 Загальна інформація\n\n")
            f.write(f"- **Загальний розмір:** {format_bytes(usage['total'])}\n")
            f.write(f"- **Використано:** {format_bytes(usage['used'])} ({usage['percent']:.1f}%)\n")
            f.write(f"- **Вільно:** {format_bytes(usage['free'])}\n\n")

        # Топ директорій
        if results['top_directories']:
            f.write("## 📁 Топ-20 найбільших директорій\n\n")
            f.write("| Розмір | Шлях |\n")
            f.write("|--------|------|\n")
            for path, size in results['top_directories']:
                f.write(f"| {format_bytes(size)} | `{path}` |\n")
            f.write("\n")

        # Тимчасові файли
        if results['temp_files']:
            f.write("## 🗑️ Тимчасові файли\n\n")
            f.write("| Розмір | Шлях |\n")
            f.write("|--------|------|\n")
            for temp in results['temp_files']:
                f.write(f"| {format_bytes(temp['size'])} | `{temp['path']}` |\n")
            f.write("\n")

        # Типи файлів
        if results['file_types']:
            f.write("## 📄 Топ-10 типів файлів\n\n")
            f.write("| Розмір | Тип | Кількість |\n")
            f.write("|--------|-----|----------|\n")
            for ext, data in results['file_types'].items():
                f.write(f"| {format_bytes(data['size'])} | `{ext}` | {data['count']} |\n")
            f.write("\n")

        # Архіви
        if results['archives']:
            f.write("## 📦 Архіви\n\n")
            f.write("| Розмір | Файлів | Стиснення | Шлях |\n")
            f.write("|--------|--------|-----------|------|\n")
            for archive in results['archives'][:10]:
                ratio = archive.get('compression_ratio', 0)
                f.write(f"| {format_bytes(archive['size'])} | "
                       f"{archive['files_count']} | {ratio:.1f}% | "
                       f"`{archive['path']}` |\n")
            f.write("\n")

        # Категорії
        if results['categories']:
            f.write("## 🏷️ Категоризація директорій\n\n")

            categories_stats = defaultdict(lambda: {'count': 0, 'size': 0, 'active': 0, 'dirs': []})
            for dir_path, info in results['categories'].items():
                category = info['category']
                # Знаходимо розмір з top_directories
                size = next((s for p, s in results['top_directories'] if p == dir_path), 0)

                categories_stats[category]['count'] += 1
                categories_stats[category]['size'] += size
                if info['is_active']:
                    categories_stats[category]['active'] += 1
                categories_stats[category]['dirs'].append({
                    'path': dir_path,
                    'size': size,
                    'confidence': info['confidence']
                })

            f.write("### Загальна статистика\n\n")
            f.write("| Категорія | Директорій | Розмір | Активних |\n")
            f.write("|-----------|------------|--------|----------|\n")
            for category, stats in sorted(categories_stats.items(), key=lambda x: x[1]['size'], reverse=True):
                f.write(f"| {category} | {stats['count']} | "
                       f"{format_bytes(stats['size'])} | {stats['active']} |\n")
            f.write("\n")

            f.write("### Детальна інформація\n\n")
            for category, stats in sorted(categories_stats.items()):
                if stats['dirs']:
                    f.write(f"#### {category.upper()}\n\n")
                    for dir_info in sorted(stats['dirs'], key=lambda x: x['size'], reverse=True)[:5]:
                        f.write(f"- `{dir_info['path']}` - {format_bytes(dir_info['size'])} "
                               f"(впевненість: {dir_info['confidence']}%)\n")
                    f.write("\n")

        # Дублікати
        if results['duplicates']:
            total_wasted = sum(d['wasted_space'] for d in results['duplicates'])
            f.write("## 🔍 Дублікати файлів\n\n")
            f.write(f"**Знайдено груп дублікатів:** {len(results['duplicates'])}\n")
            f.write(f"**Втрачено місця:** {format_bytes(total_wasted)}\n\n")

            f.write("| Втрачено | Копій | Розмір файлу | Файли |\n")
            f.write("|----------|-------|--------------|-------|\n")
            for dup in results['duplicates'][:10]:
                files_str = '<br>'.join(f"`{f}`" for f in dup['files'][:3])
                if len(dup['files']) > 3:
                    files_str += f"<br>... та ще {len(dup['files']) - 3}"
                f.write(f"| {format_bytes(dup['wasted_space'])} | "
                       f"{dup['count']} | {format_bytes(dup['size'])} | "
                       f"{files_str} |\n")
            f.write("\n")

        f.write("---\n\n")
        f.write("*Згенеровано автоматично скриптом analyze_disk.py*\n")

    print(f"✅ Звіт збережено: {report_path}")

def analyze_all_drives(report_dir='O:/disk_reports'):
    """Аналіз всіх доступних дисків"""
    print("🔍 Пошук доступних дисків...\n")

    available_drives = []
    for letter in 'CDEFGHIJKLMNO':
        drive = f'{letter}:'
        if os.path.exists(f'{drive}/'):
            available_drives.append(drive)

    print(f"Знайдено дисків: {len(available_drives)}")
    print(f"Диски: {', '.join(available_drives)}\n")

    results = {}
    for drive in available_drives:
        print(f"\n{'='*60}")
        result = analyze_disk(drive, report_dir)
        if result:
            results[drive] = result
        print(f"{'='*60}\n")

    # Підсумковий звіт
    generate_summary_report(results, report_dir)

    return results

def generate_summary_report(all_results, report_dir):
    """Генерація підсумкового звіту"""
    report_path = os.path.join(report_dir, 'SUMMARY.md')

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Підсумковий звіт аналізу дисків\n\n")
        f.write(f"**Дата аналізу:** {datetime.now().isoformat()}\n\n")

        f.write("## 📊 Огляд всіх дисків\n\n")
        f.write("| Диск | Загальний розмір | Використано | Вільно | % використання |\n")
        f.write("|------|------------------|-------------|--------|----------------|\n")

        total_size = 0
        total_used = 0
        total_free = 0

        for drive, result in sorted(all_results.items()):
            if result['usage']:
                usage = result['usage']
                total_size += usage['total']
                total_used += usage['used']
                total_free += usage['free']

                f.write(f"| {drive} | {format_bytes(usage['total'])} | "
                       f"{format_bytes(usage['used'])} | {format_bytes(usage['free'])} | "
                       f"{usage['percent']:.1f}% |\n")

        f.write(f"| **ВСЬОГО** | {format_bytes(total_size)} | "
               f"{format_bytes(total_used)} | {format_bytes(total_free)} | "
               f"{(total_used/total_size*100):.1f}% |\n\n")

        f.write("## 📁 Детальні звіти\n\n")
        for drive in sorted(all_results.keys()):
            drive_name = drive.rstrip(':')
            f.write(f"- [{drive}]({drive_name}_drive_analysis.md)\n")

        f.write("\n---\n\n")
        f.write("*Згенеровано автоматично скриптом analyze_disk.py*\n")

    print(f"\n✅ Підсумковий звіт збережено: {report_path}")

def export_results(results, export_format, output_file):
    """
    Експортувати результати аналізу у вказаному форматі

    Args:
        results: Словник з результатами аналізу
        export_format: Формат експорту ('json', 'csv', 'html')
        output_file: Шлях до вихідного файлу
    """
    try:
        if export_format == 'json':
            export_to_json(results, output_file)
            print(f"\n✅ JSON звіт збережено: {output_file}")
        elif export_format == 'csv':
            # Для CSV конвертуємо результати в список словників
            csv_data = []
            if 'top_directories' in results:
                for dir_info in results['top_directories']:
                    csv_data.append({
                        'type': 'directory',
                        'path': dir_info['path'],
                        'size': dir_info['size']
                    })
            export_to_csv(csv_data, output_file)
            print(f"\n✅ CSV звіт збережено: {output_file}")
        elif export_format == 'html':
            export_to_html(results, output_file)
            print(f"\n✅ HTML звіт збережено: {output_file}")
    except Exception as e:
        print(f"\n❌ Помилка експорту: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Універсальний аналізатор дисків для Windows'
    )
    parser.add_argument(
        'drive',
        nargs='?',
        help='Буква диску (наприклад, C:) або --all для всіх дисків'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Аналізувати всі доступні диски'
    )
    parser.add_argument(
        '--report-dir',
        default='O:/disk_reports',
        help='Директорія для збереження звітів (за замовчуванням: O:/disk_reports)'
    )
    parser.add_argument(
        '--export',
        choices=['json', 'csv', 'html'],
        help='Формат експорту звіту (json, csv, html)'
    )
    parser.add_argument(
        '--output',
        help='Шлях до вихідного файлу для експорту'
    )

    args = parser.parse_args()

    # Перевірка що --export та --output використовуються разом
    if args.export and not args.output:
        parser.error("--export потребує --output")
    if args.output and not args.export:
        parser.error("--output потребує --export")

    if args.all:
        analyze_all_drives(args.report_dir)
    elif args.drive:
        results = analyze_disk(args.drive, args.report_dir)

        # Експорт якщо вказано
        if args.export and args.output:
            export_results(results, args.export, args.output)
    else:
        parser.print_help()
        print("\nПриклади використання:")
        print("  python analyze_disk.py C:")
        print("  python analyze_disk.py D: --report-dir O:/reports")
        print("  python analyze_disk.py --all")
        print("  python analyze_disk.py C: --export json --output report.json")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nАналіз перервано користувачем")
    except Exception as e:
        print(f"\n\nПомилка: {e}")
        import traceback
        traceback.print_exc()
