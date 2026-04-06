# DiskDataAnalyzer v0.7.0 - Consolidation & Quality Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

> **CRITICAL:** ЗАВЖДИ починати кожну задачу з `/using-superpowers` skill для правильного роутингу worker agents!

**Current Version:** 0.5.0
**Target Version:** 0.7.0
**Status:** ⏳ Planned (0/9 tasks completed)

**Goal:** Консолідувати кодову базу, покращити якість тестування (>90% coverage), створити повну документацію, зібрати бінарники для всіх релізів.

**Architecture:** 
- Code cleanup and refactoring
- Integration and performance testing
- API and architecture documentation
- Binary builds for Windows (PyInstaller)

**Tech Stack:** 
- Testing: unittest, coverage.py
- Documentation: Sphinx, Markdown
- Build: PyInstaller, NSIS
- CI/CD: GitHub Actions

**Skills Required:**
- `/using-superpowers` - ОБОВ'ЯЗКОВО на початку кожної задачі
- `/code-simplifier` - для cleanup та refactoring
- `/test-driven-development` - для нових тестів
- `/verification-before-completion` - перед кожним комітом
- `/code-reviewer` - після завершення кожної фази

---

## Phase 7.1: Code Cleanup

### Task 7.1.1: Remove Dead Code

**Skills:** `/using-superpowers` → code-simplifier → verification-before-completion

**Files:**
- Audit: All `src/**/*.py` files
- Modify: Files with dead code
- Update: Corresponding tests

**Step 1: Використати `/using-superpowers` skill**

ОБОВ'ЯЗКОВО на початку задачі!

**Step 2: Audit codebase for dead code**

```bash
# Find unused imports
pylint src --disable=all --enable=unused-import

# Find unused variables
pylint src --disable=all --enable=unused-variable

# Find commented-out code
grep -r "^#.*def \|^#.*class " src/
```

**Step 3: Create removal checklist**

Document all dead code found:
- Unused functions
- Unused classes
- Commented-out code
- Unused imports
- Unreachable code

**Step 4: Remove dead code systematically**

For each item:
1. Verify it's truly unused (grep for references)
2. Remove the code
3. Run tests to ensure no breakage
4. Commit atomically

**Step 5: Use `/verification-before-completion` skill**

Verify all tests still pass.

**Step 6: Commit**

```bash
git add src/
git commit -m "refactor(cleanup): remove dead code

Removed:
- X unused functions
- Y unused classes
- Z commented-out code blocks
- N unused imports

All tests passing: 178+

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 7.1.2: Consolidate Duplicate Functionality

**Skills:** `/using-superpowers` → code-simplifier → verification-before-completion

**Files:**
- Audit: All `src/**/*.py` files
- Create: `src/core/utils/` (if needed)
- Modify: Files with duplicate code

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Identify duplicate code patterns**

Look for:
- Duplicate file size formatting
- Duplicate hash calculation
- Duplicate path handling
- Duplicate error handling

**Step 3: Extract common utilities**

Create shared utility modules:
```python
# src/core/utils/formatting.py
def format_size(size: int) -> str:
    """Format bytes to human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"

# src/core/utils/hashing.py
def calculate_file_hash(file_path: str, algorithm='md5') -> str:
    """Calculate file hash"""
    import hashlib
    hash_obj = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()
```

**Step 4: Refactor to use shared code**

Replace duplicate implementations with utility calls.

**Step 5: Use `/verification-before-completion` skill**

**Step 6: Commit**

```bash
git add src/
git commit -m "refactor(utils): consolidate duplicate functionality

Extracted common utilities:
- format_size() - used in X places
- calculate_file_hash() - used in Y places
- [other utilities]

Reduced code duplication by Z lines.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 7.1.3: Refactor for Consistency

**Skills:** `/using-superpowers` → code-simplifier → verification-before-completion

**Files:**
- Modify: All `src/**/*.py` files
- Create: `docs/CODE_STYLE.md`

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Create code style guide**

Document standards:
- Naming conventions (snake_case for functions, PascalCase for classes)
- Error handling patterns (try/except/finally)
- Logging patterns (logger.info/warning/error)
- Docstring format (Google style)

**Step 3: Apply consistent naming**

Standardize:
- Function names
- Variable names
- Class names
- Module names

**Step 4: Apply consistent error handling**

```python
# Standard pattern
try:
    result = operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
finally:
    cleanup()
```

**Step 5: Apply consistent logging**

```python
logger = logging.getLogger(__name__)

logger.debug("Detailed info for debugging")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
```

**Step 6: Use `/verification-before-completion` skill**

**Step 7: Commit**

```bash
git add src/ docs/CODE_STYLE.md
git commit -m "refactor(style): standardize code style and patterns

Applied consistent:
- Naming conventions
- Error handling patterns
- Logging patterns
- Docstring format

Created CODE_STYLE.md guide.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Phase 7.2: Testing Improvements

### Task 7.2.1: Add Integration Tests

**Skills:** `/using-superpowers` → test-engineer → verification-before-completion

**Files:**
- Create: `tests/integration/`
- Create: `tests/integration/test_full_workflow.py`
- Create: `tests/integration/test_gui_integration.py`
- Create: `tests/integration/test_llm_integration.py`

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Write integration test for full workflow**

```python
# tests/integration/test_full_workflow.py
import unittest
import tempfile
import os
from src.core.file_classifier import FileClassifier
from src.core.classification_cache import ClassificationCache

class TestFullWorkflow(unittest.TestCase):
    def test_classify_with_cache(self):
        """Test full classification workflow with caching"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            test_file = os.path.join(tmpdir, "document.pdf")
            with open(test_file, 'wb') as f:
                f.write(b'%PDF-1.4')
            
            # First classification (cache miss)
            classifier = FileClassifier()
            result1 = classifier.classify(test_file)
            self.assertEqual(result1['category'], 'document')
            
            # Second classification (cache hit)
            result2 = classifier.classify(test_file)
            self.assertEqual(result2, result1)
            
            # Verify cache was used
            stats = classifier.cache.get_stats()
            self.assertGreater(stats['hits'], 0)
```

**Step 3: Write GUI integration tests**

Test tab switching, data flow between tabs, etc.

**Step 4: Write LLM integration tests**

Test LLM provider fallback, cache integration, etc.

**Step 5: Run all integration tests**

```bash
python -m unittest discover -s tests/integration -v
```

**Step 6: Use `/verification-before-completion` skill**

**Step 7: Commit**

```bash
git add tests/integration/
git commit -m "test(integration): add integration tests for workflows

Added integration tests:
- Full classification workflow with caching
- GUI tab integration
- LLM provider integration

All tests passing.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 7.2.2: Add Performance Tests

**Skills:** `/using-superpowers` → test-engineer → verification-before-completion

**Files:**
- Create: `tests/performance/`
- Create: `tests/performance/test_large_datasets.py`
- Create: `tests/performance/benchmarks.py`

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Write performance benchmarks**

```python
# tests/performance/benchmarks.py
import time
import tempfile
import os

def benchmark_file_classification(num_files=1000):
    """Benchmark file classification speed"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        files = []
        for i in range(num_files):
            file_path = os.path.join(tmpdir, f"file_{i}.txt")
            with open(file_path, 'w') as f:
                f.write(f"content {i}")
            files.append(file_path)
        
        # Benchmark
        from src.core.file_classifier import FileClassifier
        classifier = FileClassifier()
        
        start = time.time()
        for file_path in files:
            classifier.classify(file_path)
        elapsed = time.time() - start
        
        print(f"Classified {num_files} files in {elapsed:.2f}s")
        print(f"Speed: {num_files/elapsed:.2f} files/sec")
        
        return elapsed
```

**Step 3: Test with large datasets**

Test with 1K, 10K, 100K files.

**Step 4: Identify bottlenecks**

Profile slow operations.

**Step 5: Document performance baselines**

Create `docs/PERFORMANCE.md` with benchmarks.

**Step 6: Use `/verification-before-completion` skill**

**Step 7: Commit**

```bash
git add tests/performance/ docs/PERFORMANCE.md
git commit -m "test(perf): add performance tests and benchmarks

Added performance tests:
- File classification benchmark
- Large dataset tests (1K, 10K files)
- Bottleneck identification

Documented performance baselines.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 7.2.3: Increase Coverage to >90%

**Skills:** `/using-superpowers` → test-engineer → verification-before-completion

**Files:**
- Modify: `tests/**/*.py` (add missing tests)
- Create: `.coveragerc` (coverage configuration)

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Measure current coverage**

```bash
pip install coverage
coverage run -m unittest discover -s tests
coverage report
coverage html
```

**Step 3: Identify untested code**

```bash
coverage report --show-missing
```

**Step 4: Add missing tests**

For each untested module/function:
1. Write failing test
2. Verify test fails
3. Verify test passes (code already exists)
4. Commit

**Step 5: Verify coverage target**

```bash
coverage report
# Target: >90% coverage
```

**Step 6: Use `/verification-before-completion` skill**

**Step 7: Commit**

```bash
git add tests/ .coveragerc
git commit -m "test(coverage): increase test coverage to >90%

Added tests for previously untested code:
- Module X: Y new tests
- Module Z: N new tests

Coverage: X% → 90%+

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Phase 7.3: Documentation

### Task 7.3.1: API Documentation

**Skills:** `/using-superpowers` → docs-updater → verification-before-completion

**Files:**
- Modify: All `src/**/*.py` (add/improve docstrings)
- Create: `docs/api/` (Sphinx docs)
- Create: `docs/conf.py` (Sphinx config)

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Add docstrings to all public APIs**

```python
def classify_file(self, filename: str, context: dict) -> dict:
    """
    Classify a file using LLM.
    
    Args:
        filename: Name of the file to classify
        context: Additional context (size, extension, parent_dir)
    
    Returns:
        dict: Classification result with keys:
            - category (str): File category
            - subcategory (str, optional): Specific type
            - description_uk (str): Ukrainian description
            - confidence (float): Confidence score 0.0-1.0
    
    Raises:
        ValueError: If filename is empty
        RuntimeError: If LLM API fails
    
    Example:
        >>> provider = ClaudeProvider(api_key="...")
        >>> result = provider.classify_file("setup.exe", {"size": 1024})
        >>> print(result['category'])
        'installer'
    """
```

**Step 3: Generate Sphinx documentation**

```bash
pip install sphinx sphinx-rtd-theme
sphinx-quickstart docs
sphinx-apidoc -o docs/api src
cd docs && make html
```

**Step 4: Publish to GitHub Pages**

Configure GitHub Actions to build and deploy docs.

**Step 5: Use `/verification-before-completion` skill**

**Step 6: Commit**

```bash
git add src/ docs/
git commit -m "docs(api): add comprehensive API documentation

Added docstrings to all public APIs:
- All modules documented
- All classes documented
- All public functions documented

Generated Sphinx documentation.
Published to GitHub Pages.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 7.3.2: Architecture Documentation

**Skills:** `/using-superpowers` → docs-updater → verification-before-completion

**Files:**
- Create: `docs/ARCHITECTURE.md`
- Create: `docs/diagrams/` (architecture diagrams)

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Document system architecture**

```markdown
# Architecture

## Overview

DiskDataAnalyzer follows a layered architecture:

```
┌─────────────────────────────────────┐
│         GUI Layer (Tkinter)         │
│  - MainWindow                       │
│  - Tabs (Classifier, Tree, etc.)   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│       Business Logic Layer          │
│  - FileClassifier                   │
│  - DirectoryTree                    │
│  - FolderCompare                    │
│  - JunkDetector                     │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│         Data Layer                  │
│  - ClassificationCache (SQLite)     │
│  - LLM Providers                    │
│  - File System Operations           │
└─────────────────────────────────────┘
```

## Components

### GUI Layer
- **MainWindow**: Main application window with notebook
- **Tabs**: Individual feature tabs (7 total)
- **Workers**: Background threads for non-blocking operations

### Business Logic Layer
- **FileClassifier**: Hybrid classification (patterns + LLM)
- **DirectoryTree**: Recursive tree building
- **FolderCompare**: Hash-based comparison
- **JunkDetector**: Multi-category junk detection

### Data Layer
- **ClassificationCache**: SQLite-based result caching
- **LLM Providers**: 4 providers with plugin architecture
- **File System**: Cross-platform file operations

## Design Patterns

- **Plugin Architecture**: LLMRegistry for extensible providers
- **Singleton**: Database connections
- **Observer**: GUI updates from background threads
- **Strategy**: Different LLM providers
- **Factory**: Provider creation

## Data Flow

1. User selects folder in GUI
2. GUI spawns background worker thread
3. Worker calls business logic (e.g., FileClassifier)
4. Business logic checks cache
5. If cache miss, calls LLM provider
6. Result cached and returned
7. Worker updates GUI via thread-safe callback
```

**Step 3: Create architecture diagrams**

Use Mermaid or PlantUML for diagrams.

**Step 4: Document design decisions**

Why certain patterns were chosen, trade-offs, etc.

**Step 5: Use `/verification-before-completion` skill**

**Step 6: Commit**

```bash
git add docs/ARCHITECTURE.md docs/diagrams/
git commit -m "docs(arch): add architecture documentation

Documented:
- System architecture (3 layers)
- Component descriptions
- Design patterns used
- Data flow diagrams
- Design decisions and trade-offs

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 7.3.3: Contributing Guide

**Skills:** `/using-superpowers` → docs-updater → verification-before-completion

**Files:**
- Create: `CONTRIBUTING.md`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`
- Create: `.github/ISSUE_TEMPLATE/bug_report.md`
- Create: `.github/ISSUE_TEMPLATE/feature_request.md`

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Create CONTRIBUTING.md**

```markdown
# Contributing to DiskDataAnalyzer

## Development Setup

1. Clone repository:
```bash
git clone https://github.com/yourusername/DiskDataAnalyzer.git
cd DiskDataAnalyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Run tests:
```bash
python -m unittest discover -s tests -v
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- See `docs/CODE_STYLE.md` for details

## Testing

- Write tests for all new code (TDD)
- Maintain >90% coverage
- Run full test suite before PR

## Pull Request Process

1. Create feature branch: `git checkout -b feature/my-feature`
2. Write tests (RED)
3. Implement feature (GREEN)
4. Refactor (REFACTOR)
5. Run tests: `python -m unittest discover -s tests -v`
6. Commit: `git commit -m "feat(scope): description"`
7. Push: `git push origin feature/my-feature`
8. Create PR with template

## Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Types: feat, fix, docs, style, refactor, test, chore

## Code Review

- All PRs require review
- Address review comments
- Squash commits before merge
```

**Step 3: Create PR template**

**Step 4: Create issue templates**

**Step 5: Use `/verification-before-completion` skill**

**Step 6: Commit**

```bash
git add CONTRIBUTING.md .github/
git commit -m "docs(contrib): add contributing guide and templates

Created:
- CONTRIBUTING.md with development setup
- Pull request template
- Bug report template
- Feature request template

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Phase 7.4: Binary Builds & Release

### Task 7.4.1: Build Binaries for v0.5.0 (Retroactive)

**Skills:** `/using-superpowers` → feature-implementer → verification-before-completion

**Files:**
- Create: `build/` (build scripts)
- Create: `build/build_windows.py`
- Create: `DiskDataAnalyzer.spec` (PyInstaller spec)

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Create PyInstaller spec**

```python
# DiskDataAnalyzer.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'anthropic',
        'openai',
        'ollama',
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
    icon='assets/icon.ico',
)
```

**Step 3: Build Windows executable**

```bash
pip install pyinstaller
pyinstaller DiskDataAnalyzer.spec
```

**Step 4: Test executable**

```bash
dist/DiskDataAnalyzer.exe
```

**Step 5: Create release archive**

```bash
cd dist
zip -r DiskDataAnalyzer-v0.5.0-windows-x64.zip DiskDataAnalyzer.exe
```

**Step 6: Upload to GitHub Release v0.5.0**

```bash
gh release upload v0.5.0 DiskDataAnalyzer-v0.5.0-windows-x64.zip
```

**Step 7: Use `/verification-before-completion` skill**

**Step 8: Commit build scripts**

```bash
git add build/ DiskDataAnalyzer.spec
git commit -m "build: add PyInstaller build configuration

Created:
- DiskDataAnalyzer.spec for PyInstaller
- build/build_windows.py script
- Built binary for v0.5.0

Binary uploaded to GitHub Release v0.5.0.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 7.4.2: Create GitHub Release v0.7.0 with Binary

**Skills:** `/using-superpowers` → verification-before-completion

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Update version to 0.7.0**

```python
# src/__init__.py
__version__ = '0.7.0'
```

**Step 3: Update CHANGELOG.md**

Add v0.7.0 section with all changes.

**Step 4: Update VERSION_HISTORY.md**

Add v0.7.0 release notes.

**Step 5: Run full test suite**

```bash
python -m unittest discover -s tests -v
coverage run -m unittest discover -s tests
coverage report
```

Expected: All tests pass, coverage >90%

**Step 6: Build binary**

```bash
pyinstaller DiskDataAnalyzer.spec
cd dist && zip -r DiskDataAnalyzer-v0.7.0-windows-x64.zip DiskDataAnalyzer.exe
```

**Step 7: Create git tag**

```bash
git tag -a v0.7.0 -m "Release v0.7.0 - Consolidation & Quality

Added:
- Code cleanup and refactoring
- Integration and performance tests
- Test coverage >90%
- Complete API documentation
- Architecture documentation
- Contributing guide
- Binary builds for all releases

Technical:
- 9 tasks completed
- Coverage: 90%+
- Performance benchmarks documented"
```

**Step 8: Push tag**

```bash
git push origin v0.7.0
```

**Step 9: Create GitHub Release**

```bash
gh release create v0.7.0 \
  --title "v0.7.0 - Consolidation & Quality" \
  --notes-file CHANGELOG.md \
  dist/DiskDataAnalyzer-v0.7.0-windows-x64.zip
```

**Step 10: Verify release**

```bash
gh release view v0.7.0
```

---

## Verification Checklist

**Перед кожним комітом ОБОВ'ЯЗКОВО:**
- [ ] Використано `/using-superpowers` skill на початку
- [ ] Використано відповідний worker agent
- [ ] Всі тести проходять
- [ ] Coverage >90% (Phase 7.2.3+)
- [ ] Використано `/verification-before-completion`
- [ ] Коміт створено з чітким повідомленням

**Перед релізом v0.7.0 ОБОВ'ЯЗКОВО:**
- [ ] Всі 9 задач Phase 7 завершені
- [ ] CHANGELOG.md оновлено
- [ ] VERSION_HISTORY.md оновлено
- [ ] Версія оновлена в `src/__init__.py`
- [ ] Всі тести проходять
- [ ] Coverage >90%
- [ ] Бінарник зібрано та протестовано
- [ ] Git tag створено
- [ ] GitHub Release створено з бінарником

---

## Progress Tracking

### Phase 7.1: Code Cleanup
- ⏳ Task 7.1.1: Remove Dead Code
- ⏳ Task 7.1.2: Consolidate Duplicate Functionality
- ⏳ Task 7.1.3: Refactor for Consistency

### Phase 7.2: Testing Improvements
- ⏳ Task 7.2.1: Add Integration Tests
- ⏳ Task 7.2.2: Add Performance Tests
- ⏳ Task 7.2.3: Increase Coverage to >90%

### Phase 7.3: Documentation
- ⏳ Task 7.3.1: API Documentation
- ⏳ Task 7.3.2: Architecture Documentation
- ⏳ Task 7.3.3: Contributing Guide

### Phase 7.4: Binary Builds & Release
- ⏳ Task 7.4.1: Build Binaries for v0.5.0 (Retroactive)
- ⏳ Task 7.4.2: Create GitHub Release v0.7.0 with Binary

**Current Status:** 0/11 tasks completed (0%)

**Note:** Phase 7.4 додано для збірки бінарників (2 додаткові задачі)
