# CLI Improvements Phase 1 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Покращити CLI функціонал DiskDataAnalyzer з оптимізацією продуктивності, розширеним аналізом та експортом звітів

**Architecture:** Додаємо багатопотоковість для швидкого сканування, систему кешування результатів, прогрес-бар для UX, підтримку додаткових форматів архівів, та експортери для різних форматів звітів. CLI отримує кольоровий вивід та інтерактивний режим.

**Tech Stack:** Python 3.7+, threading, colorama, tqdm, rarfile, py7zr, jinja2, reportlab

---

## Task 1: Прогрес-бар для CLI

**Files:**
- Create: `src/core/progress.py`
- Create: `tests/test_progress.py`
- Modify: `src/core/analyze_disk.py`

**Step 1: Write the failing test**

```python
# tests/test_progress.py
import unittest
from src.core.progress import ProgressBar

class TestProgressBar(unittest.TestCase):
    def test_create_progress_bar(self):
        pb = ProgressBar(total=100, desc="Test")
        self.assertEqual(pb.total, 100)
        self.assertEqual(pb.current, 0)
    
    def test_update_progress(self):
        pb = ProgressBar(total=100, desc="Test")
        pb.update(50)
        self.assertEqual(pb.current, 50)
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_progress -v`
Expected: FAIL with "No module named 'src.core.progress'"

**Step 3: Write minimal implementation**

```python
# src/core/progress.py
"""Прогрес-бар для CLI"""

class ProgressBar:
    def __init__(self, total, desc="Progress"):
        self.total = total
        self.current = 0
        self.desc = desc
    
    def update(self, n=1):
        self.current += n
        if self.current > self.total:
            self.current = self.total
    
    def close(self):
        pass
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_progress -v`
Expected: PASS

**Step 5: Integrate with tqdm**

```python
# src/core/progress.py
from tqdm import tqdm

class ProgressBar:
    def __init__(self, total, desc="Progress"):
        self.total = total
        self.desc = desc
        self.pbar = tqdm(total=total, desc=desc, unit="items")
        self.current = 0
    
    def update(self, n=1):
        self.pbar.update(n)
        self.current += n
    
    def close(self):
        self.pbar.close()
```

**Step 6: Update requirements.txt**

```bash
echo "tqdm>=4.65.0" >> requirements.txt
```

**Step 7: Commit**

```bash
git add src/core/progress.py tests/test_progress.py requirements.txt
git commit -m "feat(cli): add progress bar with tqdm support"
```

---

## Task 2: Кольоровий вивід CLI

**Files:**
- Create: `src/cli/colors.py`
- Create: `tests/test_colors.py`
- Modify: `src/core/analyze_disk.py`

**Step 1: Write the failing test**

```python
# tests/test_colors.py
import unittest
from src.cli.colors import colorize, Colors

class TestColors(unittest.TestCase):
    def test_colorize_success(self):
        result = colorize("Success", Colors.GREEN)
        self.assertIn("Success", result)
    
    def test_colorize_error(self):
        result = colorize("Error", Colors.RED)
        self.assertIn("Error", result)
```

**Step 2: Run test**

Run: `python -m unittest tests.test_colors -v`
Expected: FAIL

**Step 3: Implement colors module**

```python
# src/cli/colors.py
"""Кольоровий вивід для CLI"""
from colorama import init, Fore, Style

init(autoreset=True)

class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL

def colorize(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def success(text):
    return colorize(f"✅ {text}", Colors.GREEN)

def error(text):
    return colorize(f"❌ {text}", Colors.RED)

def warning(text):
    return colorize(f"⚠️  {text}", Colors.YELLOW)

def info(text):
    return colorize(f"ℹ️  {text}", Colors.BLUE)
```

**Step 4: Run test**

Run: `python -m unittest tests.test_colors -v`
Expected: PASS

**Step 5: Update requirements.txt**

```bash
echo "colorama>=0.4.6" >> requirements.txt
```

**Step 6: Commit**

```bash
git add src/cli/colors.py tests/test_colors.py requirements.txt
git commit -m "feat(cli): add colorful output with colorama"
```

---

## Task 3: Підтримка RAR архівів

**Files:**
- Modify: `src/core/analyze_disk.py:analyze_archive()`
- Create: `tests/test_rar_archives.py`

**Step 1: Write failing test**

```python
# tests/test_rar_archives.py
import unittest
import os
import tempfile
from src.core.analyze_disk import analyze_archive

class TestRARArchives(unittest.TestCase):
    def test_rar_detection(self):
        # Потребує тестовий RAR файл
        # Поки що skip
        self.skipTest("Requires test RAR file")
```

**Step 2: Update analyze_archive function**

```python
# src/core/analyze_disk.py
import rarfile

def analyze_archive(filepath):
    result = {
        'type': None,
        'files_count': 0,
        'uncompressed_size': 0,
        'compression_ratio': 0,
        'file_list': []
    }

    try:
        # Existing ZIP/TAR code...
        
        # Add RAR support
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
        
        # Calculate compression ratio
        if result['uncompressed_size'] > 0:
            compressed_size = os.path.getsize(filepath)
            result['compression_ratio'] = (1 - compressed_size / result['uncompressed_size']) * 100

    except Exception as e:
        result['error'] = str(e)

    return result
```

**Step 3: Update requirements.txt**

```bash
echo "rarfile>=4.0" >> requirements.txt
```

**Step 4: Commit**

```bash
git add src/core/analyze_disk.py tests/test_rar_archives.py requirements.txt
git commit -m "feat(archives): add RAR archive support"
```

---

## Task 4: Підтримка 7z архівів

**Files:**
- Modify: `src/core/analyze_disk.py:analyze_archive()`
- Create: `tests/test_7z_archives.py`

**Step 1: Update analyze_archive for 7z**

```python
# src/core/analyze_disk.py
import py7zr

def analyze_archive(filepath):
    # ... existing code ...
    
    try:
        # Add 7z support
        if filepath.endswith('.7z'):
            result['type'] = '7z'
            with py7zr.SevenZipFile(filepath, 'r') as zf:
                for name, info in zf.list():
                    if not info.is_directory:
                        result['files_count'] += 1
                        result['uncompressed_size'] += info.uncompressed
                        result['file_list'].append({
                            'name': name,
                            'size': info.uncompressed
                        })
    except Exception as e:
        result['error'] = str(e)
    
    return result
```

**Step 2: Update requirements.txt**

```bash
echo "py7zr>=0.20.0" >> requirements.txt
```

**Step 3: Commit**

```bash
git add src/core/analyze_disk.py requirements.txt
git commit -m "feat(archives): add 7z archive support"
```

---

## Task 5: Пошук великих файлів

**Files:**
- Create: `src/core/large_files.py`
- Create: `tests/test_large_files.py`
- Modify: `src/core/analyze_disk.py`

**Step 1: Write failing test**

```python
# tests/test_large_files.py
import unittest
import tempfile
import os
from src.core.large_files import find_large_files

class TestLargeFiles(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    
    def test_find_large_files(self):
        # Create test files
        large_file = os.path.join(self.test_dir, 'large.bin')
        with open(large_file, 'wb') as f:
            f.write(b'0' * (10 * 1024 * 1024))  # 10MB
        
        result = find_large_files(self.test_dir, min_size=5*1024*1024, limit=10)
        self.assertEqual(len(result), 1)
        self.assertGreaterEqual(result[0]['size'], 10*1024*1024)
```

**Step 2: Run test**

Run: `python -m unittest tests.test_large_files -v`
Expected: FAIL

**Step 3: Implement large_files module**

```python
# src/core/large_files.py
"""Пошук великих файлів"""
import os

def find_large_files(path, min_size=100*1024*1024, limit=100):
    """
    Знайти найбільші файли
    
    Args:
        path: Шлях для пошуку
        min_size: Мінімальний розмір файлу (за замовчуванням 100MB)
        limit: Максимальна кількість результатів
    
    Returns:
        List[dict]: Список файлів з інформацією
    """
    large_files = []
    
    try:
        for root, dirs, files in os.walk(path):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    size = os.path.getsize(filepath)
                    if size >= min_size:
                        large_files.append({
                            'path': filepath,
                            'size': size,
                            'name': filename
                        })
                except (PermissionError, FileNotFoundError, OSError):
                    pass
    except (PermissionError, FileNotFoundError, OSError):
        pass
    
    # Sort by size descending
    large_files.sort(key=lambda x: x['size'], reverse=True)
    
    return large_files[:limit]
```

**Step 4: Run test**

Run: `python -m unittest tests.test_large_files -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/core/large_files.py tests/test_large_files.py
git commit -m "feat(analysis): add large files finder"
```

---

## Task 6: JSON експортер

**Files:**
- Create: `src/core/exporters/__init__.py`
- Create: `src/core/exporters/json_exporter.py`
- Create: `tests/test_json_exporter.py`

**Step 1: Write failing test**

```python
# tests/test_json_exporter.py
import unittest
import json
import tempfile
import os
from src.core.exporters.json_exporter import export_to_json

class TestJSONExporter(unittest.TestCase):
    def test_export_to_json(self):
        data = {
            'drive': 'C:',
            'usage': {'total': 1000, 'used': 500, 'free': 500}
        }
        
        output_file = tempfile.mktemp(suffix='.json')
        export_to_json(data, output_file)
        
        self.assertTrue(os.path.exists(output_file))
        
        with open(output_file, 'r') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded['drive'], 'C:')
        os.unlink(output_file)
```

**Step 2: Run test**

Expected: FAIL

**Step 3: Implement JSON exporter**

```python
# src/core/exporters/json_exporter.py
"""JSON експортер для звітів"""
import json

def export_to_json(data, output_path):
    """
    Експортувати дані в JSON
    
    Args:
        data: Словник з даними аналізу
        output_path: Шлях до вихідного файлу
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
```

**Step 4: Run test**

Expected: PASS

**Step 5: Commit**

```bash
git add src/core/exporters/ tests/test_json_exporter.py
git commit -m "feat(export): add JSON exporter"
```

---

## Task 7: CSV експортер

**Files:**
- Create: `src/core/exporters/csv_exporter.py`
- Create: `tests/test_csv_exporter.py`

**Step 1: Implement CSV exporter**

```python
# src/core/exporters/csv_exporter.py
"""CSV експортер для звітів"""
import csv

def export_to_csv(data, output_path):
    """
    Експортувати дані в CSV
    
    Args:
        data: Словник з даними аналізу
        output_path: Шлях до вихідного файлу
    """
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow(['Metric', 'Value'])
        
        # Usage info
        if 'usage' in data:
            writer.writerow(['Total Size', data['usage'].get('total', 0)])
            writer.writerow(['Used', data['usage'].get('used', 0)])
            writer.writerow(['Free', data['usage'].get('free', 0)])
        
        # Top directories
        if 'top_directories' in data:
            writer.writerow([])
            writer.writerow(['Directory', 'Size'])
            for path, size in data['top_directories']:
                writer.writerow([path, size])
```

**Step 2: Commit**

```bash
git add src/core/exporters/csv_exporter.py tests/test_csv_exporter.py
git commit -m "feat(export): add CSV exporter"
```

---

## Task 8: HTML експортер

**Files:**
- Create: `src/core/exporters/html_exporter.py`
- Create: `src/core/exporters/templates/report.html`
- Create: `tests/test_html_exporter.py`

**Step 1: Create HTML template**

```html
<!-- src/core/exporters/templates/report.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Disk Analysis Report - {{ drive }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Disk Analysis Report: {{ drive }}</h1>
    <p><strong>Date:</strong> {{ timestamp }}</p>
    
    <h2>Usage Information</h2>
    <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Total Size</td><td>{{ usage.total }}</td></tr>
        <tr><td>Used</td><td>{{ usage.used }}</td></tr>
        <tr><td>Free</td><td>{{ usage.free }}</td></tr>
        <tr><td>Percentage</td><td>{{ usage.percent }}%</td></tr>
    </table>
    
    <h2>Top Directories</h2>
    <table>
        <tr><th>Path</th><th>Size</th></tr>
        {% for path, size in top_directories %}
        <tr><td>{{ path }}</td><td>{{ size }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
```

**Step 2: Implement HTML exporter**

```python
# src/core/exporters/html_exporter.py
"""HTML експортер для звітів"""
from jinja2 import Template
import os

def export_to_html(data, output_path):
    """
    Експортувати дані в HTML
    
    Args:
        data: Словник з даними аналізу
        output_path: Шлях до вихідного файлу
    """
    template_path = os.path.join(
        os.path.dirname(__file__),
        'templates',
        'report.html'
    )
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = Template(f.read())
    
    html = template.render(**data)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
```

**Step 3: Update requirements.txt**

```bash
echo "jinja2>=3.1.0" >> requirements.txt
```

**Step 4: Commit**

```bash
git add src/core/exporters/html_exporter.py src/core/exporters/templates/ requirements.txt
git commit -m "feat(export): add HTML exporter with Jinja2 templates"
```

---

## Task 9: Інтеграція експортерів в CLI

**Files:**
- Modify: `src/core/analyze_disk.py:main()`

**Step 1: Add export argument**

```python
# src/core/analyze_disk.py
def main():
    parser = argparse.ArgumentParser(
        description='Універсальний аналізатор дисків для Windows'
    )
    # ... existing arguments ...
    
    parser.add_argument(
        '--export',
        choices=['json', 'csv', 'html', 'all'],
        help='Експортувати звіт в додатковому форматі'
    )
    
    args = parser.parse_args()
    
    # ... existing code ...
    
    # Export if requested
    if args.export and results:
        from core.exporters.json_exporter import export_to_json
        from core.exporters.csv_exporter import export_to_csv
        from core.exporters.html_exporter import export_to_html
        
        drive_name = results['drive'].rstrip(':')
        
        if args.export in ['json', 'all']:
            json_path = os.path.join(args.report_dir, f'{drive_name}_analysis.json')
            export_to_json(results, json_path)
            print(f"✅ JSON exported: {json_path}")
        
        if args.export in ['csv', 'all']:
            csv_path = os.path.join(args.report_dir, f'{drive_name}_analysis.csv')
            export_to_csv(results, csv_path)
            print(f"✅ CSV exported: {csv_path}")
        
        if args.export in ['html', 'all']:
            html_path = os.path.join(args.report_dir, f'{drive_name}_analysis.html')
            export_to_html(results, html_path)
            print(f"✅ HTML exported: {html_path}")
```

**Step 2: Test manually**

```bash
python src/core/analyze_disk.py O: --export json
python src/core/analyze_disk.py O: --export all
```

**Step 3: Commit**

```bash
git add src/core/analyze_disk.py
git commit -m "feat(cli): integrate exporters with --export argument"
```

---

## Task 10: Update documentation

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/DEVELOPMENT_PLAN.md`

**Step 1: Update README with new features**

```markdown
# README.md additions

## New Features (v0.2.0)

### Export Formats
```bash
# Export to JSON
python src/core/analyze_disk.py C: --export json

# Export to CSV
python src/core/analyze_disk.py C: --export csv

# Export to HTML
python src/core/analyze_disk.py C: --export html

# Export to all formats
python src/core/analyze_disk.py C: --export all
```

### Archive Support
- ZIP ✅
- TAR/TAR.GZ ✅
- RAR ✅ (new)
- 7Z ✅ (new)

### CLI Improvements
- Colorful output
- Progress bars
- Large files detection
```

**Step 2: Update CHANGELOG**

```markdown
# CHANGELOG.md

## [0.2.0] - 2026-04-06

### Added
- Progress bars for long operations (tqdm)
- Colorful CLI output (colorama)
- RAR archive support
- 7z archive support
- Large files finder
- JSON export
- CSV export
- HTML export with templates
- --export CLI argument

### Changed
- Improved performance with progress feedback
- Better UX with colored output

### Dependencies
- tqdm>=4.65.0
- colorama>=0.4.6
- rarfile>=4.0
- py7zr>=0.20.0
- jinja2>=3.1.0
```

**Step 3: Commit**

```bash
git add README.md CHANGELOG.md docs/DEVELOPMENT_PLAN.md
git commit -m "docs: update documentation for v0.2.0 features"
```

---

## Final Steps

**Step 1: Run all tests**

```bash
python -m unittest discover -s tests -v
```

Expected: All tests pass

**Step 2: Test on real drive**

```bash
python src/core/analyze_disk.py O: --export all
```

**Step 3: Create release tag**

```bash
git tag -a v0.2.0 -m "Release v0.2.0: CLI improvements"
```

**Step 4: Update version**

```python
# src/__init__.py
__version__ = '0.2.0'
```

---

## Success Criteria

- ✅ All tests pass
- ✅ Progress bars work
- ✅ Colorful output displays correctly
- ✅ RAR and 7z archives analyzed
- ✅ Large files detected
- ✅ JSON/CSV/HTML export works
- ✅ Documentation updated
- ✅ No regressions in existing features

---

**Total estimated time:** 1 week (5-7 days)
**Tasks:** 10 main tasks
**New files:** ~15
**Modified files:** ~5
