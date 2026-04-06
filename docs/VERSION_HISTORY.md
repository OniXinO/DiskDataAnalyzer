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
- **LLM-based file classification** with 4 providers (Claude, OpenAI, Ollama, KiroAI)
- **Plugin architecture** with LLMRegistry for extensibility
- **SQLite-based classification cache** with automatic invalidation
- **Directory tree visualization** with filtering and Unicode export
- **Folder comparison** with hash-based detection (MD5)
- **Extended junk detection** with 5 categories and safe deletion
- **4 new GUI tabs** integrated into application

**Technical:**
- 10 new core modules
- 178 tests (all passing, 3 skipped)
- Full TDD coverage
- Thread-safe GUI updates
- Graceful degradation for optional dependencies

**Commits:** d61c840...07bc983

---

### v0.4.0 (Partially Implemented) - Advanced Features

**Implemented Features:**
- Disk snapshots and comparison
- Periodic analysis scheduler with APScheduler
- PDF export with ReportLab
- Safe duplicate deletion with interactive selection

**Status:** Features implemented but not formally released as v0.4.0

**Note:** These features exist in codebase but were not part of a versioned release.

---

### v0.3.0 (Partially Implemented) - GUI Implementation

**Implemented Features:**
- Tkinter main window with notebook
- Drive selection tab with combobox
- Results visualization tab with matplotlib
- Export tab for JSON/CSV/HTML
- Threaded analysis worker (non-blocking UI)

**Status:** Features implemented but not formally released as v0.3.0

**Note:** GUI foundation exists, enhanced in v0.5.0 with 4 additional tabs.

---

### v0.2.0 (Partially Implemented) - CLI Improvements

**Implemented Features:**
- Enhanced CLI arguments (--export, --output)
- Multiple export formats integration
- Improved error handling

**Status:** Features implemented but not formally released as v0.2.0

**Note:** CLI improvements exist in codebase.

---

### v0.1.0 (Initial) - Basic Disk Analysis

**Features:**
- Basic disk usage analysis
- Top directories finder (top 20)
- File type analysis and categorization
- Archive analysis (ZIP, TAR, TAR.GZ, TAR.BZ2, TAR.XZ, RAR, 7Z)
- Directory categorization (project, backup, media, game, document, system)
- Duplicate finder (MD5 hash-based)
- Large files finder (configurable threshold)
- Export formats: Markdown, JSON, CSV, HTML

**Status:** ✅ Completed (baseline functionality)

---

## Upcoming Releases

### v0.6.0 (Next) - Integration & Documentation

**Planned:**
- GUI integration (all tabs in main window)
- GitHub Actions CI/CD workflows
- Comprehensive user guide
- Application entry point (run.py)
- Manual testing checklist
- CHANGELOG.md creation
- GitHub releases for v0.5.0 and v0.6.0

**Target Date:** 2026-04-07

**Tasks:** 9 tasks in Phase 6

---

### v0.7.0 (Planned) - Consolidation

**Planned:**
- Code cleanup and dead code removal
- Consolidate duplicate functionality
- Refactor for consistency
- Integration tests
- Performance tests
- Test coverage >90%
- API documentation
- Architecture documentation
- Contributing guide

**Target Date:** 2026-04-14

**Tasks:** 9 tasks in Phase 7

---

### v1.0.0 (Future) - Production Ready

**Requirements:**
- Security audit
- Performance optimization
- Error handling review
- UI/UX improvements
- Accessibility compliance (WCAG)
- Internationalization (i18n)
- Beta testing
- Release candidate
- Stable API
- Complete documentation

**Target Date:** TBD

**Tasks:** 9 tasks in Phase 8

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
| 0.7.0 | Phase 7 | Consolidation | ⏳ Planned |
| 1.0.0 | Phase 8 | Production ready | ⏳ Future |

**Note:** Phases 2, 3, 4 were partially implemented but not formally released. Phase 5 (v0.5.0) is the first complete phase release with full TDD coverage.

---

## Development Statistics

### Current (v0.5.0)
- **Total Commits:** 30+
- **Total Tests:** 178 (3 skipped)
- **Test Coverage:** High (TDD methodology)
- **Core Modules:** 20+
- **GUI Tabs:** 7 (3 original + 4 new)
- **Supported Formats:** 10+ (archives, exports)

### Roadmap Progress
- **Total Tasks Planned:** 37
- **Completed:** 10 (27%)
- **Remaining:** 27 (73%)
- **Current Phase:** 6 of 8

---

## Breaking Changes

### v0.5.0
- None (backward compatible with v0.1.0 core functionality)

### Future (v1.0.0)
- API stabilization may introduce breaking changes
- Will be documented in CHANGELOG.md before release

---

## Deprecation Notices

### Current
- No deprecations

### Future
- TBD based on API stabilization in v1.0.0

---

## Support Policy

- **Current Release (v0.5.0):** Active development
- **Previous Releases:** No formal support (pre-release versions)
- **v1.0.0+:** Will establish LTS policy

---

## Release Process

### Pre-1.0.0 (Current)
1. Complete phase tasks
2. Update version in `src/__init__.py`
3. Update `VERSION_HISTORY.md`
4. Update `CHANGELOG.md`
5. Run full test suite
6. Create git tag
7. Create GitHub release

### Post-1.0.0 (Future)
- Will include beta/RC process
- Formal release notes
- Migration guides for breaking changes

---

## Version History Maintenance

This file is updated with each release. For detailed changes, see:
- `CHANGELOG.md` - Detailed changelog
- `docs/plans/` - Implementation plans
- Git commit history - Complete change log

Last updated: 2026-04-06
