"""
Тести для розширеного детектора сміття
"""

import unittest
import os
import sys
import tempfile
import shutil
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.junk_detector import JunkDetector


class TestJunkDetector(unittest.TestCase):
    """Тести для JunkDetector"""

    def setUp(self):
        """Створити тимчасову структуру для тестування"""
        self.temp_dir = tempfile.mkdtemp()

        # Тимчасові файли
        open(os.path.join(self.temp_dir, "file.tmp"), 'w').close()
        open(os.path.join(self.temp_dir, "cache.cache"), 'w').close()

        # Backup файли
        with open(os.path.join(self.temp_dir, "data.bak"), 'w') as f:
            f.write("backup")

        # Старий backup (створити та змінити mtime)
        old_backup = os.path.join(self.temp_dir, "old.backup")
        with open(old_backup, 'w') as f:
            f.write("old backup")
        # Встановити mtime на 100 днів назад
        old_time = time.time() - (100 * 24 * 60 * 60)
        os.utime(old_backup, (old_time, old_time))

        # Дублікати
        with open(os.path.join(self.temp_dir, "duplicate1.txt"), 'w') as f:
            f.write("same content")
        with open(os.path.join(self.temp_dir, "duplicate2.txt"), 'w') as f:
            f.write("same content")

        # Унікальний файл
        with open(os.path.join(self.temp_dir, "unique.txt"), 'w') as f:
            f.write("unique content")

        # Порожня папка
        os.makedirs(os.path.join(self.temp_dir, "empty_folder"))

        # Непорожня папка
        os.makedirs(os.path.join(self.temp_dir, "not_empty"))
        open(os.path.join(self.temp_dir, "not_empty", "file.txt"), 'w').close()

        # Системний файл (для whitelist)
        open(os.path.join(self.temp_dir, "system32.dll"), 'w').close()

    def tearDown(self):
        """Видалити тимчасову структуру"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_detect_temp_files(self):
        """Тест виявлення тимчасових файлів"""
        detector = JunkDetector(self.temp_dir)
        result = detector.detect()

        self.assertIn("temp_files", result)
        temp_files = [os.path.basename(f) for f in result["temp_files"]]
        self.assertIn("file.tmp", temp_files)
        self.assertIn("cache.cache", temp_files)

    def test_detect_backup_files(self):
        """Тест виявлення backup файлів"""
        detector = JunkDetector(self.temp_dir)
        result = detector.detect()

        self.assertIn("backup_files", result)
        backup_files = [os.path.basename(f) for f in result["backup_files"]]
        self.assertIn("data.bak", backup_files)

    def test_detect_old_backups(self):
        """Тест виявлення застарілих backup файлів"""
        detector = JunkDetector(self.temp_dir, old_backup_days=30)
        result = detector.detect()

        self.assertIn("old_backups", result)
        old_backups = [os.path.basename(f) for f in result["old_backups"]]
        self.assertIn("old.backup", old_backups)

    def test_detect_duplicates(self):
        """Тест виявлення дублікатів за hash"""
        detector = JunkDetector(self.temp_dir)
        result = detector.detect()

        self.assertIn("duplicates", result)
        # duplicates має бути список груп дублікатів
        self.assertIsInstance(result["duplicates"], list)

        # Знайти групу з duplicate1.txt та duplicate2.txt
        found_group = False
        for group in result["duplicates"]:
            basenames = [os.path.basename(f) for f in group]
            if "duplicate1.txt" in basenames and "duplicate2.txt" in basenames:
                found_group = True
                break

        self.assertTrue(found_group, "Duplicates not detected")

    def test_detect_empty_folders(self):
        """Тест виявлення порожніх папок"""
        detector = JunkDetector(self.temp_dir)
        result = detector.detect()

        self.assertIn("empty_folders", result)
        empty_folders = [os.path.basename(f) for f in result["empty_folders"]]
        self.assertIn("empty_folder", empty_folders)
        self.assertNotIn("not_empty", empty_folders)

    def test_whitelist_system_files(self):
        """Тест що системні файли не позначаються як сміття"""
        detector = JunkDetector(self.temp_dir,
                               system_whitelist=["*.dll", "system32*"])
        result = detector.detect()

        # system32.dll не має бути в temp_files
        all_junk = []
        for category in result.values():
            if isinstance(category, list):
                all_junk.extend(category)
            elif isinstance(category, list) and category:  # duplicates
                for group in category:
                    all_junk.extend(group)

        junk_basenames = [os.path.basename(f) for f in all_junk if isinstance(f, str)]
        self.assertNotIn("system32.dll", junk_basenames)

    def test_is_safe_to_delete(self):
        """Тест перевірки безпечності видалення"""
        detector = JunkDetector(self.temp_dir)

        # Тимчасовий файл - безпечно
        temp_file = os.path.join(self.temp_dir, "file.tmp")
        self.assertTrue(detector.is_safe_to_delete(temp_file))

        # Системний файл - небезпечно
        detector_with_whitelist = JunkDetector(self.temp_dir,
                                               system_whitelist=["*.dll"])
        dll_file = os.path.join(self.temp_dir, "system32.dll")
        self.assertFalse(detector_with_whitelist.is_safe_to_delete(dll_file))

    def test_get_stats_returns_summary(self):
        """Тест що get_stats повертає статистику"""
        detector = JunkDetector(self.temp_dir)
        detector.detect()

        stats = detector.get_stats()

        self.assertIn("total_junk_files", stats)
        self.assertIn("total_junk_size", stats)
        self.assertIn("by_category", stats)
        self.assertIsInstance(stats["total_junk_files"], int)

    def test_detect_with_recursive_false(self):
        """Тест не-рекурсивного сканування"""
        # Створити вкладену структуру
        nested_dir = os.path.join(self.temp_dir, "nested")
        os.makedirs(nested_dir)
        open(os.path.join(nested_dir, "nested.tmp"), 'w').close()

        detector = JunkDetector(self.temp_dir, recursive=False)
        result = detector.detect()

        # Вкладений файл не має бути знайдений
        all_files = []
        for category in result.values():
            if isinstance(category, list) and category and isinstance(category[0], str):
                all_files.extend(category)

        nested_found = any("nested.tmp" in f for f in all_files)
        self.assertFalse(nested_found)

    def test_detect_returns_dict_with_all_categories(self):
        """Тест що detect повертає всі категорії"""
        detector = JunkDetector(self.temp_dir)
        result = detector.detect()

        expected_categories = [
            "temp_files",
            "backup_files",
            "old_backups",
            "duplicates",
            "empty_folders"
        ]

        for category in expected_categories:
            self.assertIn(category, result)


if __name__ == '__main__':
    unittest.main()
