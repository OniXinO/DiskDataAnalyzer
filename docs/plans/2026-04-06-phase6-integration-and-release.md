# DiskDataAnalyzer v0.5.0 → v0.6.0 - Integration & Release Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

> **CRITICAL:** ЗАВЖДИ починати кожну задачу з `/using-superpowers` skill для правильного роутингу worker agents!

**Current Version:** 0.5.0
**Target Version:** 0.6.0
**Status:** ⏳ Planned (0/9 tasks completed)

**Goal:** Інтегрувати 4 нові GUI вкладки в головне вікно, провести повне тестування, оновити документацію, створити GitHub релізи для v0.5.0 та v0.6.0.

**Architecture:** 
- Інтеграція нових вкладок в MainWindow
- Повне інтеграційне тестування GUI
- Автоматизація GitHub релізів
- Оновлення документації

**Tech Stack:** 
- GUI: Tkinter
- Testing: unittest
- CI/CD: GitHub Actions
- Release: GitHub Releases API (gh CLI)

**Skills Required:**
- `/using-superpowers` - ОБОВ'ЯЗКОВО на початку кожної задачі
- `/test-driven-development` - для всіх задач з кодом
- `/verification-before-completion` - перед кожним комітом
- `/code-reviewer` - після завершення кожної фази

---

## Phase 6.1: GUI Integration (v0.5.0 completion)

### Task 6.1.1: Integrate New Tabs into MainWindow

**Skills:** `/using-superpowers` → test-engineer → feature-implementer → verification-before-completion

**Files:**
- Modify: `src/gui/main_window.py`
- Create: `tests/test_main_window_integration.py`

**Step 1: Використати `/using-superpowers` skill**

ОБОВ'ЯЗКОВО на початку задачі!

**Step 2: Write failing test**

```python
import unittest
import tkinter as tk
from gui.main_window import MainWindow

class TestMainWindowIntegration(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.window = MainWindow(self.root)
    
    def tearDown(self):
        self.root.destroy()
    
    def test_has_classifier_tab(self):
        """Тест що є вкладка File Classifier"""
        tabs = [self.window.notebook.tab(i, "text") for i in range(self.window.notebook.index("end"))]
        self.assertIn("File Classifier", tabs)
    
    def test_has_tree_tab(self):
        """Тест що є вкладка Directory Tree"""
        tabs = [self.window.notebook.tab(i, "text") for i in range(self.window.notebook.index("end"))]
        self.assertIn("Directory Tree", tabs)
    
    def test_has_compare_tab(self):
        """Тест що є вкладка Folder Compare"""
        tabs = [self.window.notebook.tab(i, "text") for i in range(self.window.notebook.index("end"))]
        self.assertIn("Folder Compare", tabs)
    
    def test_has_junk_tab(self):
        """Тест що є вкладка Junk Detector"""
        tabs = [self.window.notebook.tab(i, "text") for i in range(self.window.notebook.index("end"))]
        self.assertIn("Junk Detector", tabs)
```

**Step 3: Run test to verify it fails**

Run: `python -m unittest tests.test_main_window_integration -v`
Expected: FAIL (tabs not added)

**Step 4: Write minimal implementation**

Modify `src/gui/main_window.py`:

```python
from gui.classifier_tab import ClassifierTab
from gui.tree_tab import TreeTab
from gui.compare_tab import CompareTab
from gui.junk_tab import JunkTab

def _create_widgets(self):
    """Створення віджетів"""
    # Notebook для вкладок
    self.notebook = ttk.Notebook(self.root)
    self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Існуючі вкладки (якщо є)
    # ...
    
    # Нові вкладки Phase 5
    self.classifier_tab = ClassifierTab(self.notebook)
    self.notebook.add(self.classifier_tab, text="File Classifier")
    
    self.tree_tab = TreeTab(self.notebook)
    self.notebook.add(self.tree_tab, text="Directory Tree")
    
    self.compare_tab = CompareTab(self.notebook)
    self.notebook.add(self.compare_tab, text="Folder Compare")
    
    self.junk_tab = JunkTab(self.notebook)
    self.notebook.add(self.junk_tab, text="Junk Detector")
```

**Step 5: Run test to verify it passes**

Run: `python -m unittest tests.test_main_window_integration -v`
Expected: PASS

**Step 6: Use `/verification-before-completion` skill**

Verify all tests pass before commit.

**Step 7: Commit**

```bash
git add src/gui/main_window.py tests/test_main_window_integration.py
git commit -m "feat(gui): integrate 4 new tabs into main window

Added tabs:
- File Classifier (LLM-based classification)
- Directory Tree (hierarchical visualization)
- Folder Compare (diff two folders)
- Junk Detector (safe cleanup)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6.1.2: Manual GUI Testing

**Skills:** `/using-superpowers` → test-engineer → verification-before-completion

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Create manual test checklist**

Create: `docs/testing/manual-gui-test-checklist.md`

```markdown
# Manual GUI Testing Checklist

## File Classifier Tab
- [ ] Folder selection works
- [ ] LLM provider dropdown shows available providers
- [ ] Scan button starts classification
- [ ] Progress bar updates during scan
- [ ] Results table populates correctly
- [ ] Export to CSV works
- [ ] Export to JSON works

## Directory Tree Tab
- [ ] Folder selection works
- [ ] Ignore patterns input works
- [ ] Max depth dropdown works
- [ ] Build button creates tree
- [ ] TreeView displays hierarchy correctly
- [ ] Icons show for folders/files
- [ ] Export to text works
- [ ] Statistics display correctly

## Folder Compare Tab
- [ ] Both folder selections work
- [ ] Compare button starts comparison
- [ ] Results show with correct colors (green/orange/blue/red)
- [ ] Statistics display correctly
- [ ] Export report works

## Junk Detector Tab
- [ ] Folder selection works
- [ ] All 5 checkboxes work
- [ ] Recursive checkbox works
- [ ] Scan button finds junk
- [ ] Results table shows files with types and sizes
- [ ] Safe delete button works with confirmation
- [ ] Statistics display correctly
- [ ] Warning message visible

## Integration
- [ ] All tabs accessible from notebook
- [ ] Switching between tabs works smoothly
- [ ] No crashes or errors
- [ ] Memory usage reasonable
```

**Step 3: Perform manual testing**

Run application and test each item in checklist.

**Step 4: Document results**

Update checklist with ✅ or ❌ for each item.

**Step 5: Commit checklist**

```bash
git add docs/testing/manual-gui-test-checklist.md
git commit -m "docs(testing): add manual GUI test checklist

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6.1.3: Update README with New Features

**Skills:** `/using-superpowers` → docs-updater → verification-before-completion

**Files:**
- Modify: `README.md`

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Update README**

Add new features section:

```markdown
### ✅ LLM-Based File Classification (v0.5.0)
- 4 LLM провайдери: Claude, OpenAI, Ollama, KiroAI
- Гібридна класифікація (90% patterns, 10% LLM)
- SQLite кешування результатів
- Експорт в CSV/JSON

### ✅ Directory Tree Visualization (v0.5.0)
- Рекурсивна побудова дерева
- Фільтрація за patterns
- Unicode візуалізація (├── └── │)
- Експорт в текст

### ✅ Folder Comparison (v0.5.0)
- Hash-based порівняння (MD5)
- Виявлення: identical, different, only_in_first, only_in_second
- Кольорове виділення результатів
- Текстовий звіт

### ✅ Extended Junk Detection (v0.5.0)
- 5 категорій: temp files, backups, old backups, duplicates, empty folders
- Whitelist системних файлів
- Безпечне видалення з підтвердженням
- Статистика звільненого місця
```

**Step 3: Commit**

```bash
git add README.md
git commit -m "docs(readme): add Phase 5 features to README

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Phase 6.2: GitHub Release v0.5.0

### Task 6.2.1: Create CHANGELOG.md

**Skills:** `/using-superpowers` → docs-updater → verification-before-completion

**Files:**
- Create: `CHANGELOG.md`

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Create CHANGELOG**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-04-06

### Added
- **LLM-Based File Classification**
  - 4 LLM providers: Claude API, OpenAI API, Ollama (local), KiroAI+omniroute
  - Plugin architecture with LLMRegistry for extensibility
  - Hybrid classification: 90% pattern-based, 10% LLM fallback
  - SQLite-based classification cache with invalidation
  - GUI tab with provider selection and CSV/JSON export

- **Directory Tree Visualization**
  - Recursive tree building with max_depth control
  - Ignore patterns with glob-style matching
  - Unicode tree export (├── └── │)
  - GUI tab with TreeView widget and statistics

- **Folder Comparison**
  - Hash-based comparison (MD5, 8KB chunks)
  - Detects: identical, different, only_in_first, only_in_second
  - Fallback to size/mtime comparison
  - GUI tab with color-coded results (green/orange/blue/red)

- **Extended Junk Detection**
  - 5 detection categories: temp_files, backup_files, old_backups, duplicates, empty_folders
  - System whitelist with glob pattern matching
  - Safe deletion checks
  - GUI tab with confirmation dialog and statistics

### Changed
- Integrated 4 new tabs into main GUI window
- Updated README with Phase 5 features

### Technical
- 10 new core modules
- 178 tests (all passing)
- TDD methodology throughout
- Thread-safe GUI updates

## [0.4.0] - Previous release
...
```

**Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs(changelog): add CHANGELOG for v0.5.0

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6.2.2: Create Git Tag and GitHub Release v0.5.0

**Skills:** `/using-superpowers` → verification-before-completion

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Verify all tests pass**

```bash
python -m unittest discover -s tests -v
```

Expected: All tests PASS

**Step 3: Create git tag**

```bash
git tag -a v0.5.0 -m "Release v0.5.0 - Advanced Analysis Features

Added:
- LLM-based file classification (4 providers)
- Directory tree visualization
- Folder comparison
- Extended junk detection
- 4 new GUI tabs

Technical:
- 10 new modules
- 178 tests passing
- Full TDD coverage"
```

**Step 4: Push tag to GitHub**

```bash
git push origin v0.5.0
```

**Step 5: Create GitHub Release**

```bash
gh release create v0.5.0 \
  --title "v0.5.0 - Advanced Analysis Features" \
  --notes-file CHANGELOG.md \
  --latest
```

**Step 6: Verify release created**

```bash
gh release view v0.5.0
```

---

## Phase 6.3: Additional Features (v0.6.0)

### Task 6.3.1: Add Application Entry Point

**Skills:** `/using-superpowers` → test-engineer → feature-implementer → verification-before-completion

**Files:**
- Create: `run.py` (application entry point)
- Create: `tests/test_run.py`

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Write failing test**

```python
import unittest
import os

class TestRun(unittest.TestCase):
    def test_run_file_exists(self):
        """Тест що run.py існує"""
        self.assertTrue(os.path.exists("run.py"))
    
    def test_run_has_main(self):
        """Тест що run.py має main функцію"""
        with open("run.py") as f:
            content = f.read()
            self.assertIn("def main()", content)
            self.assertIn("if __name__ == '__main__'", content)
```

**Step 3: Run test to verify it fails**

**Step 4: Write minimal implementation**

Create `run.py`:

```python
#!/usr/bin/env python3
"""
DiskDataAnalyzer - Application Entry Point
"""

import tkinter as tk
from src.gui.main_window import MainWindow


def main():
    """Головна функція запуску додатку"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
```

**Step 5: Run test to verify it passes**

**Step 6: Use `/verification-before-completion` skill**

**Step 7: Commit**

```bash
git add run.py tests/test_run.py
git commit -m "feat(app): add application entry point run.py

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6.3.2: Add GitHub Actions CI/CD

**Skills:** `/using-superpowers` → feature-implementer → verification-before-completion

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `.github/workflows/release.yml`

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Create CI workflow**

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ master, dev ]
  pull_request:
    branches: [ master, dev ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m unittest discover -s tests -v
    
    - name: Check code style
      run: |
        pip install flake8
        flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
```

**Step 3: Create release workflow**

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m unittest discover -s tests -v
    
    - name: Extract version from tag
      id: get_version
      run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT
    
    - name: Create GitHub Release
      uses: softprops/action-gh-release@v1
      with:
        files: |
          CHANGELOG.md
          README.md
        body_path: CHANGELOG.md
        draft: false
        prerelease: false
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Step 4: Commit**

```bash
git add .github/workflows/ci.yml .github/workflows/release.yml
git commit -m "ci: add GitHub Actions workflows for CI and releases

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6.3.3: Add User Documentation

**Skills:** `/using-superpowers` → docs-updater → verification-before-completion

**Files:**
- Create: `docs/USER_GUIDE.md`

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Create user guide**

Create `docs/USER_GUIDE.md`:

```markdown
# DiskDataAnalyzer - User Guide

## Installation

### Requirements
- Python 3.9+
- Windows OS (primary support)
- Optional: LLM API keys for classification

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Optional LLM Providers

```bash
# For Claude API
pip install anthropic>=0.18.0

# For OpenAI API
pip install openai>=1.0.0

# For Ollama (local)
pip install ollama>=0.1.0
```

## Running the Application

```bash
python run.py
```

## Features Guide

### File Classifier Tab

1. Click "Select Folder" to choose directory
2. Select LLM provider from dropdown
3. Click "Classify" to start
4. View results in table
5. Export to CSV or JSON

**Note:** LLM classification requires API keys or local Ollama installation.

### Directory Tree Tab

1. Click "Select Folder"
2. Enter ignore patterns (comma-separated): `.git, __pycache__, node_modules`
3. Select max depth (optional)
4. Click "Build Tree"
5. Explore hierarchy in TreeView
6. Export to text file

### Folder Compare Tab

1. Select Folder 1
2. Select Folder 2
3. Check options (recursive, use hash)
4. Click "Compare"
5. View color-coded results:
   - 🟢 Green: Identical files
   - 🟠 Orange: Different content
   - 🔵 Blue: Only in Folder 1
   - 🔴 Red: Only in Folder 2
6. Export report

### Junk Detector Tab

1. Click "Select Folder"
2. Check junk types to detect:
   - Temp files (.tmp, .temp)
   - Backup files (.bak, .backup)
   - Old backups (>30 days)
   - Duplicates (same hash)
   - Empty folders
3. Check "Recursive" for subdirectories
4. Click "Scan"
5. Review results
6. Click "Safe Delete" (with confirmation)

**⚠️ Warning:** Deletion is permanent! Review carefully before deleting.

## Troubleshooting

### LLM Provider Not Available

**Problem:** "Provider not available" error

**Solution:**
- Install required library: `pip install anthropic` (or openai/ollama)
- Check API key is set
- For Ollama: ensure service is running on localhost:11434

### Slow Classification

**Problem:** File classification is slow

**Solution:**
- Use pattern-based classification (no LLM) for most files
- LLM is only used for ambiguous cases (~10%)
- Results are cached in SQLite

### Permission Errors

**Problem:** Cannot delete files

**Solution:**
- Run as Administrator (if needed)
- Check file is not in use
- System files are whitelisted and won't be deleted

## Support

- GitHub Issues: https://github.com/yourusername/DiskDataAnalyzer/issues
- Documentation: https://github.com/yourusername/DiskDataAnalyzer/docs
```

**Step 3: Commit**

```bash
git add docs/USER_GUIDE.md
git commit -m "docs(guide): add comprehensive user guide

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6.3.4: Update Version to v0.6.0

**Skills:** `/using-superpowers` → verification-before-completion

**Files:**
- Modify: `src/__init__.py`
- Modify: `CHANGELOG.md`

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Update version**

Modify `src/__init__.py`:

```python
"""
DiskDataAnalyzer - Універсальний аналізатор дисків
"""

__version__ = '0.6.0'
__author__ = 'Your Name'
__license__ = 'MIT'
```

**Step 3: Update CHANGELOG**

Add to `CHANGELOG.md`:

```markdown
## [0.6.0] - 2026-04-06

### Added
- Application entry point (`run.py`)
- GitHub Actions CI/CD workflows
- Comprehensive user guide
- Automated release process

### Changed
- Improved documentation structure
- Enhanced testing coverage

### Technical
- CI runs on Python 3.9, 3.10, 3.11, 3.12
- Automated GitHub releases on tag push
```

**Step 4: Commit**

```bash
git add src/__init__.py CHANGELOG.md
git commit -m "chore(version): bump version to 0.6.0

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Phase 6.4: GitHub Release v0.6.0

### Task 6.4.1: Create Git Tag and GitHub Release v0.6.0

**Skills:** `/using-superpowers` → verification-before-completion

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Verify all tests pass**

```bash
python -m unittest discover -s tests -v
```

**Step 3: Create git tag**

```bash
git tag -a v0.6.0 -m "Release v0.6.0 - Integration & Documentation

Added:
- Application entry point (run.py)
- GitHub Actions CI/CD
- Comprehensive user guide
- Automated release workflow

Improved:
- Documentation structure
- Testing coverage
- Release process"
```

**Step 4: Push tag to GitHub**

```bash
git push origin v0.6.0
```

**Step 5: Verify GitHub Actions triggered**

```bash
gh run list --workflow=release.yml
```

**Step 6: Verify release created**

```bash
gh release view v0.6.0
```

---

## Verification Checklist

**Перед кожним комітом ОБОВ'ЯЗКОВО:**
- [ ] Використано `/using-superpowers` skill на початку
- [ ] Використано відповідний worker agent
- [ ] Всі тести проходять
- [ ] Немає регресій
- [ ] Використано `/verification-before-completion`
- [ ] Коміт створено з чітким повідомленням

**Перед релізом ОБОВ'ЯЗКОВО:**
- [ ] Всі задачі фази завершені
- [ ] CHANGELOG.md оновлено
- [ ] README.md оновлено
- [ ] Версія оновлена в `src/__init__.py`
- [ ] Всі тести проходять (178+ tests)
- [ ] Manual GUI testing completed
- [ ] Git tag створено
- [ ] GitHub Release створено
- [ ] CI/CD workflows працюють

---

## Progress Tracking

### Phase 6.1: GUI Integration (v0.5.0 completion)
- ⏳ Task 6.1.1: Integrate New Tabs into MainWindow
- ⏳ Task 6.1.2: Manual GUI Testing
- ⏳ Task 6.1.3: Update README with New Features

### Phase 6.2: GitHub Release v0.5.0
- ⏳ Task 6.2.1: Create CHANGELOG.md
- ⏳ Task 6.2.2: Create Git Tag and GitHub Release v0.5.0

### Phase 6.3: Additional Features (v0.6.0)
- ⏳ Task 6.3.1: Add Application Entry Point
- ⏳ Task 6.3.2: Add GitHub Actions CI/CD
- ⏳ Task 6.3.3: Add User Documentation
- ⏳ Task 6.3.4: Update Version to v0.6.0

### Phase 6.4: GitHub Release v0.6.0
- ⏳ Task 6.4.1: Create Git Tag and GitHub Release v0.6.0

**Current Status:** 0/9 tasks completed (0%)

**Target Releases:**
- v0.5.0: Advanced Analysis Features (Phase 5 completion)
- v0.6.0: Integration & Documentation (Phase 6 completion)
