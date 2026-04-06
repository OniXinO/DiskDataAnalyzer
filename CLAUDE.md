# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Опис проєкту

DiskDataAnalyzer - універсальний аналізатор дисків для Windows. Проєкт створений для інвентаризації та аналізу даних на дисках з автоматичною категоризацією, аналізом архівів та пошуком дублікатів.

## Команди розробки

### Запуск аналізу
```bash
# Аналіз одного диску
python src/core/analyze_disk.py C:

# Аналіз всіх дисків
python src/core/analyze_disk.py --all

# Вказати директорію для звітів
python src/core/analyze_disk.py D: --report-dir O:/reports
```

### Тестування (майбутнє)
```bash
# Запуск всіх тестів
python -m unittest discover -s tests

# Запуск конкретного тесту
python -m unittest tests.test_analyzer
```

## Архітектура

### Структура проєкту

```
DiskDataAnalyzer/
├── src/
│   ├── core/
│   │   └── analyze_disk.py    # Основний модуль аналізу
│   ├── gui/                    # GUI компоненти (в розробці)
│   └── utils/                  # Допоміжні утиліти
├── tests/                      # Тести
├── docs/                       # Документація
├── config/                     # Конфігураційні файли
└── reports/                    # Згенеровані звіти
```

### Основні компоненти

#### 1. Аналіз дисків (`analyze_disk.py`)
- `get_disk_usage()` - інформація про використання диску
- `get_directory_size()` - рекурсивний розрахунок розміру
- `analyze_disk()` - головна функція аналізу
- `analyze_all_drives()` - аналіз всіх доступних дисків

#### 2. Аналіз архівів
- `analyze_archive()` - аналіз ZIP, TAR архівів
- Підтримка форматів: .zip, .tar, .tar.gz, .tar.bz2, .tar.xz
- Розрахунок коефіцієнта стиснення

#### 3. Категоризація
- `categorize_directory()` - визначення типу директорії
- Категорії: project, backup, media, game, document, system
- Перевірка маркерів (.git, package.json, requirements.txt)
- Визначення активності (файли змінювались останні 30 днів)

#### 4. Пошук дублікатів
- `find_duplicates()` - пошук за MD5 хешем
- `calculate_file_hash()` - обчислення хешу файлу
- Групування однакових файлів
- Розрахунок втраченого місця

#### 5. Генерація звітів
- `generate_report()` - Markdown звіт для одного диску
- `generate_summary_report()` - підсумковий звіт для всіх дисків
- Формат: таблиці, статистика, детальна інформація

## Важливі особливості

### Робота з Windows шляхами
- Використовуємо forward slashes: `C:/Windows` замість `C:\Windows`
- Підтримка WSL1 середовища
- Всі шляхи обробляються через `pathlib.Path`

### Обробка помилок
- Всі операції з файлами обгорнуті в try-except
- Ігноруємо `PermissionError`, `FileNotFoundError`, `OSError`
- Продовжуємо аналіз навіть при помилках

### Продуктивність
- Обмеження глибини сканування (`max_depth=2`)
- Аналіз типів файлів тільки для дисків < 500GB
- Пошук дублікатів тільки для дисків < 100GB
- Мінімальний розмір файлу для дублікатів: 10MB

### Категоризація директорій
Система визначає тип директорії за:
1. **Маркерами** (файли-індикатори):
   - `.git`, `.gitignore` → project
   - `package.json`, `requirements.txt` → project
   - README.md в корені → project
2. **Ключовими словами** в назві:
   - backup, bak, old → backup
   - photo, video, music → media
   - game, steam → game
3. **Типами файлів** всередині

## План розробки

**Поточний стан:** Фаза 1 (CLI) завершена ✅

**Наступні кроки:**
1. Фаза 2: GUI на Tkinter
2. Фаза 3: Розширені функції (очищення, експорт)
3. Фаза 4: Дистрибуція (.exe, інсталятор)

Детальний план: `docs/DEVELOPMENT_PLAN.md`

## Методологія розробки

**ВАЖЛИВО:** Проєкт використовує ітеративний підхід зі скілами Claude Code.

### Цикл виконання задачі:
1. Прочитати задачу з `docs/DEVELOPMENT_PLAN.md`
2. Використати відповідний skill
3. Виконати роботу
4. Використати `/verification-before-completion`
5. Отримати підтвердження
6. Зробити атомарний коміт

### Таблиця скілів:
- Нові функції → `/feature-implementer`
- Тести → `/test-driven-development`
- Рефакторинг → `/code-simplifier`
- Документація → `/docs-updater`
- Перевірка → `/verification-before-completion` (завжди перед комітом)
- Code review → `/code-reviewer` (після фази)

## Патерни та практики

### Форматування виводу
- Використовуємо `format_bytes()` для розмірів
- Emoji для категорій: 📊 📁 🗑️ 📄 📦 🏷️ 🔍
- Вирівнювання в таблицях

### Звіти
- Markdown формат для читабельності
- Таблиці для структурованих даних
- Секції з заголовками
- Посилання між звітами

### Тестування (майбутнє)
- Unit tests для кожної функції
- Mock файлової системи
- Тести з різними розмірами дисків
- Coverage > 80%

## Поточна версія

**Версія:** 0.1.0 (Alpha)  
**Дата:** 2026-04-06  
**Статус:** CLI завершено, GUI в розробці

## Залежності

Всі модулі входять в стандартну бібліотеку Python 3.7+:
- os, sys, argparse, pathlib
- shutil, datetime, collections
- hashlib, zipfile, tarfile, json

Майбутні залежності для GUI:
- tkinter (вбудований)
- pillow (зображення)
- matplotlib (графіки)
