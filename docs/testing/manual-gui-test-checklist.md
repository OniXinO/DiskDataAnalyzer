# Manual GUI Testing Checklist

**Version:** 0.5.0
**Date:** 2026-04-07
**Tester:** _____________

---

## Pre-Testing Setup

- [ ] Application launches without errors
- [ ] Window opens with correct title: "DiskDataAnalyzer v0.5.0"
- [ ] Window size: 1000x700
- [ ] All 4 tabs visible in notebook

---

## Tab 1: File Classifier

### Basic Functionality
- [ ] "Select Folder" button opens folder dialog
- [ ] Selected folder path displays in entry field
- [ ] LLM provider dropdown shows available providers
- [ ] "Classify" button is clickable

### Classification Process
- [ ] Click "Classify" starts classification
- [ ] Progress bar appears and animates
- [ ] Status text updates ("Classifying...")
- [ ] UI remains responsive during classification
- [ ] Results populate in table after completion

### Results Display
- [ ] Table has 5 columns (File, Category, Subcategory, Description, Confidence)
- [ ] File paths are relative to selected folder
- [ ] Categories are readable
- [ ] Confidence scores display correctly (0.0-1.0)

### Export Functionality
- [ ] "Export CSV" button opens save dialog
- [ ] CSV file created successfully
- [ ] CSV contains all results
- [ ] "Export JSON" button opens save dialog
- [ ] JSON file created successfully
- [ ] JSON is valid and contains all results

### Error Handling
- [ ] Clicking "Classify" without folder shows error
- [ ] Invalid folder path shows error
- [ ] Missing LLM provider shows appropriate message

**Notes:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Tab 2: Directory Tree

### Basic Functionality
- [ ] "Select Folder" button opens folder dialog
- [ ] Selected folder path displays in entry field
- [ ] Ignore patterns input accepts text
- [ ] Default ignore patterns: `.git, __pycache__, node_modules`
- [ ] Max depth dropdown shows options (Unlimited, 1, 2, 3, 5, 10)

### Tree Building
- [ ] "Build Tree" button starts building
- [ ] Progress bar appears and animates
- [ ] Status text updates ("Building tree...")
- [ ] UI remains responsive during build

### Tree Display
- [ ] TreeView displays hierarchical structure
- [ ] Root folder shown at top
- [ ] Folders have 📁 icon
- [ ] Files have 📄 icon with size
- [ ] Tree can be expanded/collapsed
- [ ] Scrollbars work (vertical and horizontal)

### Statistics
- [ ] Statistics display after build
- [ ] Shows: Files count, Folders count, Total size
- [ ] Size formatted correctly (B, KB, MB, GB)

### Export
- [ ] "Export Text" button opens save dialog
- [ ] Text file created successfully
- [ ] Text uses Unicode tree symbols (├── └── │)
- [ ] File is readable

### Filtering
- [ ] Ignore patterns work (e.g., `.git` excluded)
- [ ] Max depth limits tree depth correctly
- [ ] Changing filters and rebuilding works

**Notes:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Tab 3: Folder Compare

### Basic Functionality
- [ ] "Select Folder 1" button opens dialog
- [ ] Folder 1 path displays correctly
- [ ] "Select Folder 2" button opens dialog
- [ ] Folder 2 path displays correctly
- [ ] "Recursive" checkbox toggles
- [ ] "Use Hash" checkbox toggles
- [ ] "Compare" button is clickable

### Comparison Process
- [ ] Click "Compare" starts comparison
- [ ] Progress bar appears and animates
- [ ] Status text updates ("Comparing...")
- [ ] UI remains responsive during comparison

### Results Display
- [ ] Results table has 2 columns (File, Status)
- [ ] Color coding works:
  - [ ] Green text for "✓ Identical"
  - [ ] Orange text for "≠ Different content"
  - [ ] Blue text for "→ Only in folder 1"
  - [ ] Red text for "← Only in folder 2"
- [ ] File paths are relative
- [ ] Scrollbar works

### Statistics
- [ ] Statistics display after comparison
- [ ] Shows: Identical count, Different count, Only in 1, Only in 2
- [ ] Counts are accurate

### Export
- [ ] "Export Report" button opens save dialog
- [ ] Text report created successfully
- [ ] Report contains all differences
- [ ] Report is readable

### Options
- [ ] Recursive option includes subdirectories
- [ ] Non-recursive option only compares top level
- [ ] Hash comparison detects identical content
- [ ] Non-hash comparison uses size/mtime

**Notes:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Tab 4: Junk Detector

### Basic Functionality
- [ ] "Select Folder" button opens folder dialog
- [ ] Selected folder path displays in entry field
- [ ] 5 junk type checkboxes present:
  - [ ] Temp files
  - [ ] Backup files
  - [ ] Old backups
  - [ ] Duplicates
  - [ ] Empty folders
- [ ] All checkboxes checked by default
- [ ] "Recursive" checkbox present and checked
- [ ] "Scan" button is clickable

### Scanning Process
- [ ] Click "Scan" starts scanning
- [ ] Progress bar appears and animates
- [ ] Status text updates ("Scanning...")
- [ ] UI remains responsive during scan

### Results Display
- [ ] Results table has 3 columns (File, Type, Size)
- [ ] File paths are relative to selected folder
- [ ] Types match selected checkboxes:
  - [ ] "Temp" for temp files
  - [ ] "Backup" for backup files
  - [ ] "Old backup" for old backups
  - [ ] "Duplicate" for duplicates
  - [ ] "Empty folder" for empty folders
- [ ] Sizes formatted correctly (B, KB, MB, GB)
- [ ] Empty folders show "0 B"

### Statistics
- [ ] Statistics display after scan
- [ ] Shows: Total files found, Total size
- [ ] Counts and sizes are accurate

### Safe Delete
- [ ] "Safe Delete" button disabled before scan
- [ ] "Safe Delete" button enabled after scan with results
- [ ] Clicking "Safe Delete" shows confirmation dialog
- [ ] Confirmation shows count of files to delete
- [ ] Warning message visible: "⚠️ This operation is irreversible!"
- [ ] Clicking "Yes" deletes files
- [ ] Clicking "No" cancels deletion
- [ ] Success message shows deleted count
- [ ] Results table clears after deletion
- [ ] Statistics clear after deletion

### Filtering
- [ ] Unchecking junk types filters results
- [ ] Recursive option includes subdirectories
- [ ] Non-recursive option only scans top level
- [ ] Rescanning with different options works

### Safety
- [ ] System files are NOT included in results
- [ ] Windows directory files excluded
- [ ] Program Files files excluded
- [ ] Critical system paths protected

**Notes:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Integration Testing

### Tab Switching
- [ ] Can switch between all 4 tabs
- [ ] Tab content persists when switching
- [ ] No crashes when switching tabs
- [ ] No memory leaks (check Task Manager)

### Multiple Operations
- [ ] Can run operations in different tabs sequentially
- [ ] Previous results remain visible
- [ ] No interference between tabs

### Window Management
- [ ] Window can be resized
- [ ] Content adjusts to window size
- [ ] Scrollbars appear when needed
- [ ] Window can be minimized/maximized
- [ ] Window can be closed cleanly

### Performance
- [ ] Application starts quickly (<5 seconds)
- [ ] UI remains responsive during operations
- [ ] Memory usage reasonable (<500 MB)
- [ ] No UI freezing

**Notes:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Error Scenarios

### Invalid Input
- [ ] Empty folder path handled gracefully
- [ ] Non-existent folder shows error
- [ ] Permission denied shows error
- [ ] Invalid characters in path handled

### Edge Cases
- [ ] Empty folder handled correctly
- [ ] Very large folder (>10K files) works
- [ ] Folder with special characters works
- [ ] Network drive works (if applicable)

### Recovery
- [ ] Can recover from errors
- [ ] Can retry after error
- [ ] Application doesn't crash on error

**Notes:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Overall Assessment

### Usability
- [ ] UI is intuitive
- [ ] Buttons are clearly labeled
- [ ] Progress indicators are helpful
- [ ] Error messages are clear

### Stability
- [ ] No crashes during testing
- [ ] No unexpected errors
- [ ] Application closes cleanly

### Performance
- [ ] Operations complete in reasonable time
- [ ] UI remains responsive
- [ ] Memory usage acceptable

---

## Issues Found

| # | Tab | Issue | Severity | Notes |
|---|-----|-------|----------|-------|
| 1 |     |       |          |       |
| 2 |     |       |          |       |
| 3 |     |       |          |       |
| 4 |     |       |          |       |
| 5 |     |       |          |       |

**Severity:** Critical / High / Medium / Low

---

## Test Summary

**Total Test Cases:** 100+
**Passed:** _____
**Failed:** _____
**Blocked:** _____

**Overall Status:** ☐ Pass ☐ Fail ☐ Needs Work

**Tester Signature:** _________________ **Date:** _________

**Reviewer Signature:** _________________ **Date:** _________

---

## Recommendations

```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```
