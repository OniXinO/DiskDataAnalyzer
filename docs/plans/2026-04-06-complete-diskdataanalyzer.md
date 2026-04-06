# DiskDataAnalyzer Complete Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Complete DiskDataAnalyzer with GUI, advanced features, and Windows distribution

**Architecture:** 
- Phase 2: Tkinter GUI with matplotlib visualization, threaded analysis to prevent UI freezing
- Phase 3: PDF export with reportlab, disk cleanup with safe deletion, scheduler with APScheduler, snapshot comparison with diff algorithm
- Phase 4: PyInstaller packaging, NSIS installer, auto-update with GitHub releases API

**Tech Stack:** 
- GUI: tkinter, matplotlib, pillow
- PDF: reportlab
- Packaging: PyInstaller, NSIS
- Scheduler: APScheduler
- Testing: unittest, TDD approach

---

## Phase 2: GUI Implementation (v0.3.0)

### Task 2.1: Basic Tkinter Window

**Files:**
- Create: `src/gui/main_window.py`
- Create: `tests/test_gui_window.py`

**Step 1: Write failing test**

```python
import unittest
import tkinter as tk
from gui.main_window import MainWindow

class TestMainWindow(unittest.TestCase):
    def test_window_creation(self):
        root = tk.Tk()
        window = MainWindow(root)
        self.assertIsNotNone(window)
        self.assertEqual(window.title, "DiskDataAnalyzer")
        root.destroy()
```

**Step 2: Run test - verify fails**
```bash
python -m unittest tests.test_gui_window -v
```
Expected: ModuleNotFoundError

**Step 3: Implement minimal MainWindow**

```python
import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.title = "DiskDataAnalyzer"
        self.root.title(self.title)
        self.root.geometry("1000x700")
        self._create_widgets()
    
    def _create_widgets(self):
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
```

**Step 4: Run test - verify passes**

**Step 5: Commit**
```bash
git add src/gui/main_window.py tests/test_gui_window.py
git commit -m "feat(gui): add basic Tkinter main window"
```

---

### Task 2.2: Drive Selection Tab

**Files:**
- Modify: `src/gui/main_window.py`
- Create: `src/gui/tabs/drive_tab.py`
- Create: `tests/test_drive_tab.py`

**Step 1: Write failing test**

```python
def test_drive_tab_lists_drives(self):
    root = tk.Tk()
    tab = DriveTab(root)
    drives = tab.get_available_drives()
    self.assertIsInstance(drives, list)
    root.destroy()
```

**Step 2: Implement DriveTab**

```python
import tkinter as tk
from tkinter import ttk
import string
import os

class DriveTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        # Drive selection
        ttk.Label(self, text="Select Drive:").pack(pady=10)
        self.drive_var = tk.StringVar()
        self.drive_combo = ttk.Combobox(self, textvariable=self.drive_var)
        self.drive_combo['values'] = self.get_available_drives()
        self.drive_combo.pack(pady=5)
        
        # Analyze button
        self.analyze_btn = ttk.Button(self, text="Analyze", command=self.start_analysis)
        self.analyze_btn.pack(pady=10)
    
    def get_available_drives(self):
        drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:"
            if os.path.exists(f"{drive}/"):
                drives.append(drive)
        return drives
    
    def start_analysis(self):
        pass  # Will implement later
```

**Step 3: Commit**

---

### Task 2.3: Threaded Analysis

**Files:**
- Modify: `src/gui/tabs/drive_tab.py`
- Create: `src/gui/workers/analysis_worker.py`
- Create: `tests/test_analysis_worker.py`

**Step 1: Write failing test**

```python
def test_analysis_worker_runs_in_thread(self):
    worker = AnalysisWorker("C:", callback=lambda x: None)
    worker.start()
    self.assertTrue(worker.is_alive())
    worker.join(timeout=1)
```

**Step 2: Implement AnalysisWorker**

```python
import threading
from core.analyze_disk import analyze_disk

class AnalysisWorker(threading.Thread):
    def __init__(self, drive, callback):
        super().__init__()
        self.drive = drive
        self.callback = callback
        self.daemon = True
    
    def run(self):
        try:
            results = analyze_disk(self.drive, report_dir=None)
            self.callback(results)
        except Exception as e:
            self.callback({'error': str(e)})
```

**Step 3: Integrate into DriveTab**

```python
def start_analysis(self):
    drive = self.drive_var.get()
    if not drive:
        return
    
    self.analyze_btn.config(state='disabled', text='Analyzing...')
    worker = AnalysisWorker(drive, self.on_analysis_complete)
    worker.start()

def on_analysis_complete(self, results):
    self.analyze_btn.config(state='normal', text='Analyze')
    # Display results (implement in next task)
```

**Step 4: Commit**

---

### Task 2.4: Results Visualization with Matplotlib

**Files:**
- Create: `src/gui/tabs/results_tab.py`
- Create: `tests/test_results_tab.py`

**Step 1: Write failing test**

```python
def test_results_tab_displays_pie_chart(self):
    root = tk.Tk()
    results = {'usage': {'total': 1000, 'used': 600, 'free': 400}}
    tab = ResultsTab(root, results)
    self.assertIsNotNone(tab.figure)
    root.destroy()
```

**Step 2: Implement ResultsTab with matplotlib**

```python
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ResultsTab(ttk.Frame):
    def __init__(self, parent, results):
        super().__init__(parent)
        self.results = results
        self._create_widgets()
    
    def _create_widgets(self):
        # Create matplotlib figure
        self.figure = plt.Figure(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Draw pie chart
        self._draw_usage_chart()
    
    def _draw_usage_chart(self):
        if 'usage' not in self.results:
            return
        
        usage = self.results['usage']
        ax = self.figure.add_subplot(111)
        
        sizes = [usage['used'], usage['free']]
        labels = ['Used', 'Free']
        colors = ['#ff6b6b', '#51cf66']
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title('Disk Usage')
        self.canvas.draw()
```

**Step 3: Commit**

---

### Task 2.5: Export from GUI

**Files:**
- Create: `src/gui/tabs/export_tab.py`
- Create: `tests/test_export_tab.py`

**Step 1: Write failing test**

```python
def test_export_tab_has_format_selection(self):
    root = tk.Tk()
    tab = ExportTab(root, results={})
    self.assertIsNotNone(tab.format_var)
    self.assertIn('json', tab.format_combo['values'])
    root.destroy()
```

**Step 2: Implement ExportTab**

```python
import tkinter as tk
from tkinter import ttk, filedialog
from exporters.json_exporter import export_to_json
from exporters.csv_exporter import export_to_csv
from exporters.html_exporter import export_to_html

class ExportTab(ttk.Frame):
    def __init__(self, parent, results):
        super().__init__(parent)
        self.results = results
        self._create_widgets()
    
    def _create_widgets(self):
        ttk.Label(self, text="Export Format:").pack(pady=10)
        
        self.format_var = tk.StringVar(value='json')
        self.format_combo = ttk.Combobox(self, textvariable=self.format_var)
        self.format_combo['values'] = ['json', 'csv', 'html']
        self.format_combo.pack(pady=5)
        
        ttk.Button(self, text="Export", command=self.export_results).pack(pady=10)
    
    def export_results(self):
        format_type = self.format_var.get()
        
        filetypes = {
            'json': [('JSON files', '*.json')],
            'csv': [('CSV files', '*.csv')],
            'html': [('HTML files', '*.html')]
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=f'.{format_type}',
            filetypes=filetypes[format_type]
        )
        
        if not filename:
            return
        
        if format_type == 'json':
            export_to_json(self.results, filename)
        elif format_type == 'csv':
            export_to_csv(self.results, filename)
        elif format_type == 'html':
            export_to_html(self.results, filename)
```

**Step 3: Commit**

---

## Phase 3: Advanced Features (v0.4.0)

### Task 3.1: PDF Export with ReportLab

**Files:**
- Create: `src/exporters/pdf_exporter.py`
- Create: `tests/test_pdf_exporter.py`
- Modify: `requirements.txt` (add reportlab)

**Step 1: Write failing test**

```python
def test_pdf_export_creates_file(self):
    output_file = os.path.join(self.test_dir, 'report.pdf')
    data = {'title': 'Test Report', 'summary': {}}
    
    export_to_pdf(data, output_file)
    
    self.assertTrue(os.path.exists(output_file))
```

**Step 2: Implement PDF exporter**

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def export_to_pdf(data, output_file):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = data.get('title', 'Disk Analysis Report')
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 0.5*inch))
    
    # Summary
    if 'summary' in data:
        story.append(Paragraph('Summary', styles['Heading2']))
        for key, value in data['summary'].items():
            text = f"<b>{key}:</b> {value}"
            story.append(Paragraph(text, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
    
    doc.build(story)
```

**Step 3: Commit**

---

### Task 3.2: Disk Cleanup - Safe Duplicate Deletion

**Files:**
- Create: `src/core/cleanup.py`
- Create: `tests/test_cleanup.py`

**Step 1: Write failing test**

```python
def test_cleanup_moves_duplicates_to_trash(self):
    # Create duplicate files
    file1 = os.path.join(self.test_dir, 'file1.txt')
    file2 = os.path.join(self.test_dir, 'file2.txt')
    
    with open(file1, 'w') as f:
        f.write('content')
    with open(file2, 'w') as f:
        f.write('content')
    
    duplicates = [{'files': [file1, file2]}]
    cleanup_duplicates(duplicates, keep_first=True)
    
    self.assertTrue(os.path.exists(file1))
    self.assertFalse(os.path.exists(file2))
```

**Step 2: Implement cleanup with send2trash**

```python
from send2trash import send2trash

def cleanup_duplicates(duplicates, keep_first=True, dry_run=False):
    """
    Safely delete duplicate files by moving to trash
    
    Args:
        duplicates: List of duplicate groups
        keep_first: Keep first file in each group
        dry_run: Don't actually delete, just report
    
    Returns:
        dict: Statistics about cleanup
    """
    stats = {'deleted': 0, 'space_freed': 0, 'errors': []}
    
    for group in duplicates:
        files = group['files']
        if len(files) < 2:
            continue
        
        # Keep first, delete rest
        to_delete = files[1:] if keep_first else files[:-1]
        
        for filepath in to_delete:
            try:
                if not dry_run:
                    size = os.path.getsize(filepath)
                    send2trash(filepath)
                    stats['deleted'] += 1
                    stats['space_freed'] += size
            except Exception as e:
                stats['errors'].append({'file': filepath, 'error': str(e)})
    
    return stats
```

**Step 3: Add to requirements.txt**
```
send2trash>=1.8.0
```

**Step 4: Commit**

---

### Task 3.3: Scheduler with APScheduler

**Files:**
- Create: `src/core/scheduler.py`
- Create: `tests/test_scheduler.py`

**Step 1: Write failing test**

```python
def test_scheduler_runs_analysis_periodically(self):
    scheduler = DiskScheduler()
    
    job = scheduler.schedule_analysis(
        drive='C:',
        interval_hours=24,
        report_dir='O:/reports'
    )
    
    self.assertIsNotNone(job)
    self.assertEqual(job.trigger.interval.hours, 24)
```

**Step 2: Implement scheduler**

```python
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from core.analyze_disk import analyze_disk

class DiskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
    
    def schedule_analysis(self, drive, interval_hours, report_dir):
        """Schedule periodic disk analysis"""
        job = self.scheduler.add_job(
            func=analyze_disk,
            trigger=IntervalTrigger(hours=interval_hours),
            args=[drive, report_dir],
            id=f'analysis_{drive}',
            replace_existing=True
        )
        return job
    
    def remove_job(self, drive):
        """Remove scheduled job"""
        self.scheduler.remove_job(f'analysis_{drive}')
    
    def list_jobs(self):
        """List all scheduled jobs"""
        return self.scheduler.get_jobs()
    
    def shutdown(self):
        """Shutdown scheduler"""
        self.scheduler.shutdown()
```

**Step 3: Add to requirements.txt**
```
APScheduler>=3.10.0
```

**Step 4: Commit**

---

### Task 3.4: Snapshot Comparison

**Files:**
- Create: `src/core/snapshot.py`
- Create: `tests/test_snapshot.py`

**Step 1: Write failing test**

```python
def test_compare_snapshots_detects_changes(self):
    snapshot1 = {
        'timestamp': '2026-04-01',
        'files': {'file1.txt': 100, 'file2.txt': 200}
    }
    snapshot2 = {
        'timestamp': '2026-04-06',
        'files': {'file1.txt': 150, 'file3.txt': 300}
    }
    
    diff = compare_snapshots(snapshot1, snapshot2)
    
    self.assertIn('added', diff)
    self.assertIn('removed', diff)
    self.assertIn('modified', diff)
    self.assertEqual(diff['added'], ['file3.txt'])
    self.assertEqual(diff['removed'], ['file2.txt'])
```

**Step 2: Implement snapshot comparison**

```python
import json
from datetime import datetime

def create_snapshot(drive, output_file):
    """Create disk snapshot"""
    from core.analyze_disk import analyze_disk
    
    results = analyze_disk(drive, report_dir=None)
    
    snapshot = {
        'timestamp': datetime.now().isoformat(),
        'drive': drive,
        'usage': results.get('usage', {}),
        'top_directories': results.get('top_directories', []),
        'file_types': results.get('file_types', {})
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=2)
    
    return snapshot

def compare_snapshots(snapshot1, snapshot2):
    """Compare two snapshots and return differences"""
    diff = {
        'added': [],
        'removed': [],
        'modified': [],
        'size_change': 0
    }
    
    # Compare usage
    if 'usage' in snapshot1 and 'usage' in snapshot2:
        diff['size_change'] = snapshot2['usage'].get('used', 0) - snapshot1['usage'].get('used', 0)
    
    # Compare directories
    dirs1 = {d['path']: d['size'] for d in snapshot1.get('top_directories', [])}
    dirs2 = {d['path']: d['size'] for d in snapshot2.get('top_directories', [])}
    
    diff['added'] = list(set(dirs2.keys()) - set(dirs1.keys()))
    diff['removed'] = list(set(dirs1.keys()) - set(dirs2.keys()))
    
    for path in set(dirs1.keys()) & set(dirs2.keys()):
        if dirs1[path] != dirs2[path]:
            diff['modified'].append({
                'path': path,
                'old_size': dirs1[path],
                'new_size': dirs2[path],
                'change': dirs2[path] - dirs1[path]
            })
    
    return diff
```

**Step 3: Commit**

---

## Phase 4: Distribution (v1.0.0)

### Task 4.1: PyInstaller Configuration

**Files:**
- Create: `build/diskanalyzer.spec`
- Create: `build/build.py`

**Step 1: Create PyInstaller spec**

```python
# diskanalyzer.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../src/gui/main_window.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../src', 'src'),
        ('../README.md', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'matplotlib',
        'reportlab',
        'apscheduler',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DiskDataAnalyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../assets/icon.ico'
)
```

**Step 2: Create build script**

```python
# build.py
import subprocess
import sys
import os

def build_exe():
    """Build Windows executable with PyInstaller"""
    print("Building DiskDataAnalyzer.exe...")
    
    cmd = [
        sys.executable,
        '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        'diskanalyzer.spec'
    ]
    
    result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
    
    if result.returncode == 0:
        print("✅ Build successful!")
        print("Executable: build/dist/DiskDataAnalyzer.exe")
    else:
        print("❌ Build failed!")
        sys.exit(1)

if __name__ == '__main__':
    build_exe()
```

**Step 3: Add to requirements.txt**
```
pyinstaller>=5.10.0
```

**Step 4: Commit**

---

### Task 4.2: NSIS Installer Script

**Files:**
- Create: `build/installer.nsi`

**Step 1: Create NSIS script**

```nsis
; DiskDataAnalyzer Installer Script

!define APP_NAME "DiskDataAnalyzer"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "OniXinO"
!define APP_URL "https://github.com/OniXinO/DiskDataAnalyzer"

Name "${APP_NAME}"
OutFile "DiskDataAnalyzer-Setup-${APP_VERSION}.exe"
InstallDir "$PROGRAMFILES\${APP_NAME}"

Page directory
Page instfiles

Section "Install"
    SetOutPath "$INSTDIR"
    
    File "dist\DiskDataAnalyzer.exe"
    File "..\README.md"
    File "..\LICENSE"
    
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\DiskDataAnalyzer.exe"
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\DiskDataAnalyzer.exe"
    
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\DiskDataAnalyzer.exe"
    Delete "$INSTDIR\README.md"
    Delete "$INSTDIR\LICENSE"
    Delete "$INSTDIR\Uninstall.exe"
    
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    RMDir "$INSTDIR"
    
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
SectionEnd
```

**Step 2: Commit**

---

### Task 4.3: Auto-Update System

**Files:**
- Create: `src/core/updater.py`
- Create: `tests/test_updater.py`

**Step 1: Write failing test**

```python
def test_updater_checks_for_new_version(self):
    updater = AutoUpdater(current_version='1.0.0')
    
    latest = updater.check_for_updates()
    
    self.assertIsNotNone(latest)
    self.assertIn('version', latest)
    self.assertIn('download_url', latest)
```

**Step 2: Implement auto-updater**

```python
import requests
import json
from packaging import version

class AutoUpdater:
    def __init__(self, current_version, repo='OniXinO/DiskDataAnalyzer'):
        self.current_version = current_version
        self.repo = repo
        self.api_url = f'https://api.github.com/repos/{repo}/releases/latest'
    
    def check_for_updates(self):
        """Check GitHub for latest release"""
        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()
            
            release = response.json()
            latest_version = release['tag_name'].lstrip('v')
            
            if version.parse(latest_version) > version.parse(self.current_version):
                return {
                    'version': latest_version,
                    'download_url': release['assets'][0]['browser_download_url'] if release['assets'] else None,
                    'release_notes': release['body']
                }
            
            return None
        except Exception as e:
            return {'error': str(e)}
    
    def download_update(self, download_url, output_file):
        """Download update installer"""
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return output_file
```

**Step 3: Add to requirements.txt**
```
requests>=2.31.0
packaging>=23.0
```

**Step 4: Commit**

---

## Release Plan

### v0.3.0 - GUI Release (Phase 2) ✅ COMPLETED
**Release Date:** 2026-04-06
**Status:** All 5 tasks completed

**Features:**
- ✅ Basic Tkinter main window with notebook tabs
- ✅ Drive selection tab with available drives detection
- ✅ Threaded analysis to prevent UI freezing
- ✅ Results visualization with matplotlib pie charts
- ✅ Export tab for JSON/CSV/HTML formats

**Testing:** 88 tests passing (100%)

**Commits:** 5 atomic commits
- `feat(gui): add basic Tkinter main window`
- `feat(gui): add drive selection tab`
- `feat(gui): add threaded analysis worker`
- `feat(gui): add results visualization with matplotlib`
- `feat(gui): add export tab for JSON/CSV/HTML export`

---

### v0.4.0 - Advanced Features (Phase 3) 🔄 IN PROGRESS
**Target Date:** 2026-04-08
**Status:** 0/4 tasks completed

**Planned Features:**
- [ ] PDF export with ReportLab
- [ ] Disk cleanup with safe duplicate deletion
- [ ] Scheduled analysis with APScheduler
- [ ] Snapshot comparison for tracking changes

**Dependencies:**
- reportlab>=3.6.0
- send2trash>=1.8.0
- APScheduler>=3.10.0

---

### v1.0.0 - Production Release (Phase 4) 📦 PLANNED
**Target Date:** 2026-04-10
**Status:** 0/3 tasks completed

**Planned Features:**
- [ ] PyInstaller .exe packaging
- [ ] NSIS Windows installer
- [ ] Auto-update system with GitHub releases

**Dependencies:**
- pyinstaller>=5.10.0
- requests>=2.31.0
- packaging>=23.0

**Deliverables:**
- `DiskDataAnalyzer.exe` - Standalone executable
- `DiskDataAnalyzer-Setup-1.0.0.exe` - Windows installer
- GitHub release with auto-update support

---

## Summary

**Phase 2 (v0.3.0):** ✅ 5/5 tasks - GUI with Tkinter, visualization, threading
**Phase 3 (v0.4.0):** 🔄 0/4 tasks - PDF export, cleanup, scheduler, snapshots
**Phase 4 (v1.0.0):** 📦 0/3 tasks - PyInstaller, NSIS installer, auto-update

**Total:** 5/12 tasks completed (41.7%)

**Current Version:** v0.3.0
**Next Milestone:** v0.4.0 (Phase 3)

**Testing:** Each task includes RED-GREEN-REFACTOR cycle

**Commits:** Atomic commits after each task completion
