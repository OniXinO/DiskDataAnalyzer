# Version Audit and Fix Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

> **CRITICAL:** ЗАВЖДИ починати кожну задачу з `/using-superpowers` skill для правильного роутингу worker agents!

**Goal:** Виправити версіювання проєкту, привести у відповідність з фактичним станом розробки, створити чітку версійну стратегію.

**Problem:** 
- Поточна версія в `src/__init__.py` = 0.1.0
- Фактично завершено Phase 5 (Advanced Analysis Features)
- Плануємо релізи v0.5.0 та v0.6.0
- Версії не синхронізовані

**Solution:**
- Оновити версію до 0.5.0 (Phase 5 завершена)
- Створити версійну стратегію
- Синхронізувати всі плани

---

## Phase 0: Version Audit

### Task 0.1: Audit Current State

**Skills:** `/using-superpowers` → task-planner → verification-before-completion

**Step 1: Використати `/using-superpowers` skill**

ОБОВ'ЯЗКОВО на початку задачі!

**Step 2: Document current state**

**Current Version:** 0.1.0 (in `src/__init__.py`)

**Completed Work:**
- ✅ Phase 1: CLI improvements (v0.2.0 planned)
- ✅ Phase 2: GUI implementation (v0.3.0 planned)
- ✅ Phase 3: Advanced features (v0.4.0 planned)
- ✅ Phase 5: Advanced Analysis Features (v0.5.0 - JUST COMPLETED)
  - 10 tasks completed
  - 178 tests passing
  - 4 new GUI tabs
  - LLM integration

**Planned Work:**
- ⏳ Phase 6: Integration & Release (v0.6.0)

**Version Mismatch:**
- Code says: 0.1.0
- Reality: Phase 5 completed = should be 0.5.0

**Step 3: Create version strategy**

**Semantic Versioning Strategy:**
```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes (1.0.0 = production ready)
MINOR: New features (backward compatible)
PATCH: Bug fixes (backward compatible)
```

**Project Versioning:**
```
0.1.0 - Initial release (basic disk analysis)
0.2.0 - CLI improvements
0.3.0 - GUI implementation
0.4.0 - Advanced features (snapshots, scheduler, PDF export)
0.5.0 - Advanced Analysis Features (LLM, tree, compare, junk) ← CURRENT
0.6.0 - Integration & Documentation (CI/CD, user guide) ← NEXT
1.0.0 - Production ready (stable API, full testing)
```

**Step 4: Document findings**

Create: `docs/VERSION_HISTORY.md`

---

## Phase 1: Fix Current Version

### Task 1.1: Update Version to 0.5.0

**Skills:** `/using-superpowers` → feature-implementer → verification-before-completion

**Files:**
- Modify: `src/__init__.py`

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Update version**

```python
"""
DiskDataAnalyzer - Універсальний аналізатор дисків для Windows

Основний пакет проєкту
"""

__version__ = '0.5.0'  # Changed from 0.1.0
__author__ = 'Created with Claude Code CLI'
__license__ = 'MIT'
```

**Step 3: Verify version accessible**

```python
import src
assert src.__version__ == '0.5.0'
```

**Step 4: Use `/verification-before-completion` skill**

**Step 5: Commit**

```bash
git add src/__init__.py
git commit -m "chore(version): update version to 0.5.0

Reflects completion of Phase 5 (Advanced Analysis Features):
- LLM-based file classification (4 providers)
- Directory tree visualization
- Folder comparison
- Extended junk detection
- 4 new GUI tabs
- 178 tests passing

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 1.2: Create VERSION_HISTORY.md

**Skills:** `/using-superpowers` → docs-updater → verification-before-completion

**Files:**
- Create: `docs/VERSION_HISTORY.md`

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Create version history**

```markdown
# Version History

## Version Strategy

DiskDataAnalyzer follows [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes (1.0.0 = production ready)
MINOR: New features (backward compatible)
PATCH: Bug fixes (backward compatible)
```

## Release History

### v0.5.0 (2026-04-06) - Advanced Analysis Features ✅ CURRENT

**Major Features:**
- LLM-based file classification with 4 providers (Claude, OpenAI, Ollama, KiroAI)
- Plugin architecture with LLMRegistry
- SQLite-based classification cache
- Directory tree visualization with filtering
- Folder comparison with hash-based detection
- Extended junk detection (5 categories)
- 4 new GUI tabs integrated

**Technical:**
- 10 new core modules
- 178 tests (all passing)
- Full TDD coverage
- Thread-safe GUI updates

**Commits:** d61c840...85c2f2c

---

### v0.4.0 (Planned) - Advanced Features

**Planned Features:**
- Disk snapshots and comparison
- Periodic analysis scheduler
- PDF export with ReportLab
- Safe duplicate deletion

**Status:** Partially implemented, needs consolidation

---

### v0.3.0 (Planned) - GUI Implementation

**Planned Features:**
- Tkinter main window
- Drive selection tab
- Results visualization tab
- Export tab (JSON/CSV/HTML)
- Threaded analysis worker

**Status:** Partially implemented, needs consolidation

---

### v0.2.0 (Planned) - CLI Improvements

**Planned Features:**
- Enhanced CLI arguments
- Multiple export formats
- Improved error handling

**Status:** Partially implemented, needs consolidation

---

### v0.1.0 (Initial) - Basic Disk Analysis

**Features:**
- Basic disk usage analysis
- Top directories finder
- File type analysis
- Archive analysis (ZIP, TAR, RAR, 7Z)
- Directory categorization
- Duplicate finder
- Large files finder
- Markdown/JSON/CSV/HTML export

**Status:** ✅ Completed

---

## Upcoming Releases

### v0.6.0 (Next) - Integration & Documentation

**Planned:**
- GUI integration (all tabs in main window)
- GitHub Actions CI/CD
- Comprehensive user guide
- Application entry point (run.py)
- Manual testing checklist

**Target Date:** 2026-04-07

---

### v1.0.0 (Future) - Production Ready

**Requirements:**
- Stable API
- Full test coverage (>90%)
- Complete documentation
- Performance optimization
- Security audit
- User acceptance testing

**Target Date:** TBD

---

## Version Mapping to Phases

| Version | Phase | Description | Status |
|---------|-------|-------------|--------|
| 0.1.0 | Initial | Basic disk analysis | ✅ Complete |
| 0.2.0 | Phase 1 | CLI improvements | 🔄 Partial |
| 0.3.0 | Phase 2 | GUI implementation | 🔄 Partial |
| 0.4.0 | Phase 3 | Advanced features | 🔄 Partial |
| 0.5.0 | Phase 5 | Advanced analysis | ✅ Complete |
| 0.6.0 | Phase 6 | Integration & docs | ⏳ Planned |
| 1.0.0 | Final | Production ready | ⏳ Future |

**Note:** Phases 2, 3, 4 were partially implemented but not formally released. Phase 5 (v0.5.0) is the first complete phase release.
```

**Step 3: Use `/verification-before-completion` skill**

**Step 4: Commit**

```bash
git add docs/VERSION_HISTORY.md
git commit -m "docs(version): add comprehensive version history

Documents:
- Semantic versioning strategy
- Release history (v0.1.0 to v0.5.0)
- Upcoming releases (v0.6.0, v1.0.0)
- Version to phase mapping

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 1.3: Update All Plans with Correct Versions

**Skills:** `/using-superpowers` → docs-updater → verification-before-completion

**Files:**
- Modify: `docs/plans/2026-04-06-cli-improvements-phase1.md`
- Modify: `docs/plans/2026-04-06-complete-diskdataanalyzer.md`
- Review: `docs/plans/2026-04-06-advanced-analysis-features.md` (already correct)
- Review: `docs/plans/2026-04-06-phase6-integration-and-release.md` (already correct)

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Update plan headers**

Each plan should clearly state:
```markdown
# Plan Title - vX.Y.Z

**Current Version:** 0.5.0
**Target Version:** X.Y.Z
**Status:** [Planned/In Progress/Completed]
```

**Step 3: Add version notes**

Add to each plan:
```markdown
## Version Notes

This plan targets version X.Y.Z.
Previous version: X.Y.Z
See VERSION_HISTORY.md for complete version timeline.
```

**Step 4: Use `/verification-before-completion` skill**

**Step 5: Commit**

```bash
git add docs/plans/*.md
git commit -m "docs(plans): update all plans with correct version numbers

Synchronized version numbers across all plans:
- Added version headers
- Added version notes
- Clarified target versions
- Referenced VERSION_HISTORY.md

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Phase 2: Create Comprehensive Task List

### Task 2.1: Consolidate All Remaining Tasks

**Skills:** `/using-superpowers` → task-planner → verification-before-completion

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Audit all plans**

Review all 4 plan files and extract:
- Completed tasks (mark as ✅)
- Pending tasks (mark as ⏳)
- Duplicate tasks (consolidate)
- Missing tasks (add)

**Step 3: Create master task list**

Create: `docs/MASTER_TASK_LIST.md`

```markdown
# Master Task List

## Completed Tasks ✅

### Phase 5: Advanced Analysis Features (v0.5.0)
- ✅ Task 5.1: LLM Providers with Plugin Architecture
- ✅ Task 5.2: Classification Cache
- ✅ Task 5.3: File Classifier
- ✅ Task 5.4: Directory Tree Builder
- ✅ Task 5.5: Folder Compare
- ✅ Task 5.6: Extended Junk Detector
- ✅ Task 5.7: GUI Tab - File Classifier
- ✅ Task 5.8: GUI Tab - Directory Tree
- ✅ Task 5.9: GUI Tab - Folder Compare
- ✅ Task 5.10: GUI Tab - Extended Junk Detector

**Total Completed:** 10 tasks

---

## Pending Tasks ⏳

### Phase 6: Integration & Release (v0.6.0)

#### Phase 6.1: GUI Integration
- ⏳ Task 6.1.1: Integrate New Tabs into MainWindow
- ⏳ Task 6.1.2: Manual GUI Testing
- ⏳ Task 6.1.3: Update README with New Features

#### Phase 6.2: GitHub Release v0.5.0
- ⏳ Task 6.2.1: Create CHANGELOG.md
- ⏳ Task 6.2.2: Create Git Tag and GitHub Release v0.5.0

#### Phase 6.3: Additional Features
- ⏳ Task 6.3.1: Add Application Entry Point
- ⏳ Task 6.3.2: Add GitHub Actions CI/CD
- ⏳ Task 6.3.3: Add User Documentation
- ⏳ Task 6.3.4: Update Version to v0.6.0

#### Phase 6.4: GitHub Release v0.6.0
- ⏳ Task 6.4.1: Create Git Tag and GitHub Release v0.6.0

**Total Pending (Phase 6):** 9 tasks

---

### Phase 7: Consolidation (v0.7.0) - NEW

#### Phase 7.1: Code Cleanup
- ⏳ Task 7.1.1: Remove Dead Code
- ⏳ Task 7.1.2: Consolidate Duplicate Functionality
- ⏳ Task 7.1.3: Refactor for Consistency

#### Phase 7.2: Testing Improvements
- ⏳ Task 7.2.1: Add Integration Tests
- ⏳ Task 7.2.2: Add Performance Tests
- ⏳ Task 7.2.3: Increase Coverage to >90%

#### Phase 7.3: Documentation
- ⏳ Task 7.3.1: API Documentation
- ⏳ Task 7.3.2: Architecture Documentation
- ⏳ Task 7.3.3: Contributing Guide

**Total Pending (Phase 7):** 9 tasks

---

### Phase 8: Production Ready (v1.0.0) - FUTURE

#### Phase 8.1: Stability
- ⏳ Task 8.1.1: Security Audit
- ⏳ Task 8.1.2: Performance Optimization
- ⏳ Task 8.1.3: Error Handling Review

#### Phase 8.2: Polish
- ⏳ Task 8.2.1: UI/UX Improvements
- ⏳ Task 8.2.2: Accessibility Compliance
- ⏳ Task 8.2.3: Internationalization (i18n)

#### Phase 8.3: Release
- ⏳ Task 8.3.1: Beta Testing
- ⏳ Task 8.3.2: Release Candidate
- ⏳ Task 8.3.3: v1.0.0 Release

**Total Pending (Phase 8):** 9 tasks

---

## Summary

| Phase | Version | Tasks | Status |
|-------|---------|-------|--------|
| Phase 5 | v0.5.0 | 10 | ✅ Complete |
| Phase 6 | v0.6.0 | 9 | ⏳ Next |
| Phase 7 | v0.7.0 | 9 | ⏳ Planned |
| Phase 8 | v1.0.0 | 9 | ⏳ Future |

**Total Tasks:** 37
**Completed:** 10 (27%)
**Remaining:** 27 (73%)
```

**Step 4: Use `/verification-before-completion` skill**

**Step 5: Commit**

```bash
git add docs/MASTER_TASK_LIST.md
git commit -m "docs(tasks): create master task list with all phases

Consolidated all tasks from all plans:
- Phase 5 (v0.5.0): 10 tasks ✅ Complete
- Phase 6 (v0.6.0): 9 tasks ⏳ Next
- Phase 7 (v0.7.0): 9 tasks ⏳ Planned (NEW)
- Phase 8 (v1.0.0): 9 tasks ⏳ Future

Total: 37 tasks (10 done, 27 remaining)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 2.2: Create Detailed Plans for Phase 7 and 8

**Skills:** `/using-superpowers` → writing-plans → verification-before-completion

**Step 1: Використати `/using-superpowers` skill**

**Step 2: Create Phase 7 plan**

Create: `docs/plans/2026-04-07-phase7-consolidation.md`

(Full detailed plan with all tasks, skills, TDD steps - similar to Phase 6 plan)

**Step 3: Create Phase 8 plan**

Create: `docs/plans/2026-04-08-phase8-production-ready.md`

(Full detailed plan with all tasks, skills, TDD steps - similar to Phase 6 plan)

**Step 4: Use `/verification-before-completion` skill**

**Step 5: Commit**

```bash
git add docs/plans/2026-04-07-phase7-consolidation.md docs/plans/2026-04-08-phase8-production-ready.md
git commit -m "docs(plans): add Phase 7 and Phase 8 detailed plans

Phase 7 (v0.7.0) - Consolidation:
- Code cleanup and refactoring
- Testing improvements (>90% coverage)
- Complete documentation

Phase 8 (v1.0.0) - Production Ready:
- Security audit and optimization
- UI/UX polish and accessibility
- Beta testing and release

All tasks include mandatory skills and TDD methodology.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Verification Checklist

**Перед кожним комітом ОБОВ'ЯЗКОВО:**
- [ ] Використано `/using-superpowers` skill на початку
- [ ] Використано відповідний worker agent
- [ ] Всі версії синхронізовані
- [ ] Використано `/verification-before-completion`
- [ ] Коміт створено з чітким повідомленням

---

## Progress Tracking

### Phase 0: Version Audit
- ⏳ Task 0.1: Audit Current State

### Phase 1: Fix Current Version
- ⏳ Task 1.1: Update Version to 0.5.0
- ⏳ Task 1.2: Create VERSION_HISTORY.md
- ⏳ Task 1.3: Update All Plans with Correct Versions

### Phase 2: Create Comprehensive Task List
- ⏳ Task 2.1: Consolidate All Remaining Tasks
- ⏳ Task 2.2: Create Detailed Plans for Phase 7 and 8

**Current Status:** 0/6 tasks completed (0%)
