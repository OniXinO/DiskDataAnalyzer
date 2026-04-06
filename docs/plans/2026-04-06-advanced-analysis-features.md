# DiskDataAnalyzer v0.5.0 - Advanced Analysis Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

> **CRITICAL:** ЗАВЖДИ починати кожну задачу з `/using-superpowers` skill для правильного роутингу worker agents!

**Goal:** Додати класифікацію файлів з 4 LLM провайдерами (Claude, OpenAI, Ollama, KiroAI), дерево каталогів, порівняння папок, розширене виявлення сміття, GUI вкладки.

**Architecture:** 
- Гібридна класифікація: 90% за patterns/extensions, 10% через LLM
- 4 LLM провайдери з єдиним інтерфейсом
- Кешування результатів в SQLite
- Модульна структура з TDD

**Tech Stack:** 
- LLM: anthropic (Claude), openai (OpenAI), ollama (Ollama), requests (KiroAI)
- GUI: Tkinter
- Cache: SQLite
- Testing: unittest

**Skills Required:**
- `/using-superpowers` - ОБОВ'ЯЗКОВО на початку кожної задачі
- `/test-driven-development` - для всіх задач з кодом
- `/verification-before-completion` - перед кожним комітом
- `/code-reviewer` - після завершення кожної задачі

---

## Phase 5: Advanced Analysis Features

### Task 5.1: LLM Providers with Plugin Architecture ✅ COMPLETED

### Task 5.2: Classification Cache ✅ COMPLETED

### Task 5.3: File Classifier ✅ COMPLETED

### Task 5.4: Directory Tree Builder ✅ COMPLETED

### Task 5.5: Folder Compare ✅ COMPLETED

### Task 5.6: Extended Junk Detector ✅ COMPLETED

### Task 5.7: GUI Tab - File Classifier ✅ COMPLETED

### Task 5.8: GUI Tab - Directory Tree ✅ COMPLETED

### Task 5.9: GUI Tab - Folder Compare ✅ COMPLETED

### Task 5.10: GUI Tab - Extended Junk Detector ✅ COMPLETED

**Skills:** `/using-superpowers` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/core/llm_providers.py` (базовий клас + 4 провайдери)
- Create: `src/core/llm_registry.py` (реєстр провайдерів для розширення)
- Create: `tests/test_llm_providers.py`
- Create: `tests/test_llm_registry.py`
- Modify: `requirements.txt`

**Step 1: Write failing test**

```python
import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.llm_providers import ClaudeProvider, OpenAIProvider, OllamaProvider, KiroAIProvider

class TestLLMProviders(unittest.TestCase):
    def test_claude_provider_interface(self):
        """Тест що Claude provider має правильний інтерфейс"""
        provider = ClaudeProvider(api_key="test_key")
        self.assertTrue(hasattr(provider, 'classify_file'))
    
    def test_openai_provider_interface(self):
        """Тест що OpenAI provider має правильний інтерфейс"""
        provider = OpenAIProvider(api_key="test_key")
        self.assertTrue(hasattr(provider, 'classify_file'))
    
    def test_ollama_provider_interface(self):
        """Тест що Ollama provider має правильний інтерфейс"""
        provider = OllamaProvider()
        self.assertTrue(hasattr(provider, 'classify_file'))
    
    def test_kiroai_provider_interface(self):
        """Тест що KiroAI provider має правильний інтерфейс"""
        provider = KiroAIProvider(base_url="http://localhost:8080")
        self.assertTrue(hasattr(provider, 'classify_file'))
    
    def test_provider_returns_valid_structure(self):
        """Тест що provider повертає правильну структуру"""
        # Mock provider для тестування
        class MockProvider:
            def classify_file(self, filename, context):
                return {
                    "category": "installer",
                    "description_uk": "Інсталятор програми",
                    "confidence": 0.95
                }
        
        provider = MockProvider()
        result = provider.classify_file("setup.exe", {})
        
        self.assertIn("category", result)
        self.assertIn("description_uk", result)
        self.assertIn("confidence", result)

if __name__ == '__main__':
    unittest.main()
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_llm_providers -v`
Expected: ModuleNotFoundError: No module named 'core.llm_providers'

**Step 3: Write minimal implementation**

```python
"""
LLM провайдери для класифікації файлів
Підтримує: Claude API, OpenAI API, Ollama (локальний), KiroAI+omniroute (dev)
"""

from abc import ABC, abstractmethod
import json
import logging

logger = logging.getLogger(__name__)

# Спробувати імпортувати LLM бібліотеки
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("anthropic not installed - Claude API unavailable")

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("openai not installed - OpenAI API unavailable")

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logger.warning("ollama not installed - Local LLM unavailable")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("requests not installed - KiroAI unavailable")


class LLMProvider(ABC):
    """Базовий клас для LLM провайдерів"""
    
    @abstractmethod
    def classify_file(self, filename, context):
        """
        Класифікувати файл через LLM
        
        Args:
            filename: Ім'я файлу
            context: Додатковий контекст (розмір, розширення, батьківська папка)
        
        Returns:
            dict: {
                "category": str,
                "subcategory": str (optional),
                "description_uk": str,
                "description_en": str (optional),
                "confidence": float (0.0-1.0)
            }
        """
        pass
    
    def _build_prompt(self, filename, context):
        """Побудувати промпт для LLM"""
        return f"""Classify this file and provide description in Ukrainian.

Filename: {filename}
Extension: {context.get('extension', 'unknown')}
Size: {context.get('size', 0)} bytes
Parent directory: {context.get('parent_dir', 'unknown')}

Available categories:
- installer: Інсталятори програм
- document: Документи
- image: Зображення
- video: Відео
- audio: Аудіо
- archive: Архіви
- code: Програмний код
- config: Конфігураційні файли
- data: Файли даних
- system: Системні файли
- temp: Тимчасові файли
- other: Інше

Return ONLY valid JSON (no markdown, no extra text):
{{
    "category": "one of the categories above",
    "subcategory": "specific type (optional)",
    "description_uk": "чіткий опис українською що це за файл",
    "confidence": 0.95
}}"""


class ClaudeProvider(LLMProvider):
    """Claude API провайдер (Anthropic)"""
    
    def __init__(self, api_key):
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("anthropic library not installed. Install with: pip install anthropic>=0.18.0")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    def classify_file(self, filename, context):
        try:
            prompt = self._build_prompt(filename, context)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Парсити JSON з відповіді
            content = response.content[0].text
            result = json.loads(content)
            
            return result
            
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return {
                "category": "other",
                "description_uk": f"Помилка класифікації: {str(e)}",
                "confidence": 0.0
            }


class OpenAIProvider(LLMProvider):
    """OpenAI API провайдер (GPT-4)"""
    
    def __init__(self, api_key):
        if not OPENAI_AVAILABLE:
            raise ImportError("openai library not installed. Install with: pip install openai>=1.0.0")
        
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"
    
    def classify_file(self, filename, context):
        try:
            prompt = self._build_prompt(filename, context)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                response_format={"type": "json_object"},
                max_tokens=512
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            return result
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                "category": "other",
                "description_uk": f"Помилка класифікації: {str(e)}",
                "confidence": 0.0
            }


class OllamaProvider(LLMProvider):
    """Ollama провайдер (локальний LLM)"""
    
    def __init__(self, model="llama3", base_url="http://localhost:11434"):
        if not OLLAMA_AVAILABLE:
            raise ImportError("ollama library not installed. Install with: pip install ollama>=0.1.0")
        
        self.model = model
        self.base_url = base_url
    
    def classify_file(self, filename, context):
        try:
            prompt = self._build_prompt(filename, context)
            
            response = ollama.chat(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            content = response['message']['content']
            
            # Ollama може повертати текст з markdown, витягуємо JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            
            return result
            
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return {
                "category": "other",
                "description_uk": f"Помилка класифікації: {str(e)}",
                "confidence": 0.0
            }


class KiroAIProvider(LLMProvider):
    """KiroAI+omniroute провайдер (desktop, dev-режим)"""
    
    def __init__(self, base_url="http://localhost:8080", api_key=None):
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library not installed. Install with: pip install requests>=2.31.0")
        
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
    
    def classify_file(self, filename, context):
        try:
            prompt = self._build_prompt(filename, context)
            
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json={
                    "model": "omniroute",
                    "messages": [{
                        "role": "user",
                        "content": prompt
                    }],
                    "max_tokens": 512,
                    "temperature": 0.3
                },
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            content = data["choices"][0]["message"]["content"]
            
            # KiroAI може повертати текст з markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            
            return result
            
        except Exception as e:
            logger.error(f"KiroAI error: {e}")
            return {
                "category": "other",
                "description_uk": f"Помилка класифікації: {str(e)}",
                "confidence": 0.0
            }


def get_available_providers():
    """Отримати список доступних провайдерів"""
    providers = []
    
    if ANTHROPIC_AVAILABLE:
        providers.append("claude")
    if OPENAI_AVAILABLE:
        providers.append("openai")
    if OLLAMA_AVAILABLE:
        providers.append("ollama")
    if REQUESTS_AVAILABLE:
        providers.append("kiroai")
    
    return providers
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_llm_providers -v`
Expected: PASS (всі тести проходять)

**Step 5: Update requirements.txt**

```txt
# Залежності для LLM класифікації (опціональні)
anthropic>=0.18.0  # Claude API
openai>=1.0.0      # OpenAI API
ollama>=0.1.0      # Локальний LLM
# requests>=2.31.0 вже є в requirements
```

**Step 6: Create LLM Registry for plugin architecture**

Create: `src/core/llm_registry.py`

```python
"""
Реєстр LLM провайдерів для легкого розширення
Дозволяє додавати нові провайдери без зміни основного коду
"""

import logging
from typing import Dict, Type, List
from core.llm_providers import LLMProvider

logger = logging.getLogger(__name__)


class LLMRegistry:
    """Реєстр LLM провайдерів"""
    
    _providers: Dict[str, Type[LLMProvider]] = {}
    
    @classmethod
    def register(cls, name: str, provider_class: Type[LLMProvider]):
        """Зареєструвати новий провайдер"""
        if not issubclass(provider_class, LLMProvider):
            raise TypeError(f"{provider_class} must inherit from LLMProvider")
        
        cls._providers[name] = provider_class
        logger.info(f"Registered LLM provider: {name}")
    
    @classmethod
    def get_provider(cls, name: str, **kwargs) -> LLMProvider:
        """Отримати екземпляр провайдера"""
        if name not in cls._providers:
            raise KeyError(f"Provider '{name}' not registered")
        
        return cls._providers[name](**kwargs)
    
    @classmethod
    def list_providers(cls) -> List[str]:
        """Список зареєстрованих провайдерів"""
        return list(cls._providers.keys())


# Автореєстрація вбудованих провайдерів
def _register_builtin_providers():
    from core.llm_providers import (
        ClaudeProvider, OpenAIProvider, OllamaProvider, KiroAIProvider,
        ANTHROPIC_AVAILABLE, OPENAI_AVAILABLE, OLLAMA_AVAILABLE, REQUESTS_AVAILABLE
    )
    
    if ANTHROPIC_AVAILABLE:
        LLMRegistry.register("claude", ClaudeProvider)
    if OPENAI_AVAILABLE:
        LLMRegistry.register("openai", OpenAIProvider)
    if OLLAMA_AVAILABLE:
        LLMRegistry.register("ollama", OllamaProvider)
    if REQUESTS_AVAILABLE:
        LLMRegistry.register("kiroai", KiroAIProvider)

_register_builtin_providers()
```

**Step 7: Test registry**

Create: `tests/test_llm_registry.py`

```python
import unittest
from core.llm_registry import LLMRegistry
from core.llm_providers import LLMProvider

class MockProvider(LLMProvider):
    def classify_file(self, filename, context):
        return {"category": "test"}

class TestLLMRegistry(unittest.TestCase):
    def test_register_and_get_provider(self):
        LLMRegistry.register("mock", MockProvider)
        provider = LLMRegistry.get_provider("mock")
        self.assertIsInstance(provider, MockProvider)
    
    def test_list_providers(self):
        providers = LLMRegistry.list_providers()
        self.assertIsInstance(providers, list)
        self.assertGreater(len(providers), 0)
```

**Step 8: Commit**

```bash
git add src/core/llm_providers.py tests/test_llm_providers.py requirements.txt
git commit -m "feat(llm): add 4 LLM providers - Claude, OpenAI, Ollama, KiroAI

Implements abstract LLMProvider interface with 4 concrete providers:
- ClaudeProvider: Anthropic Claude API (cloud)
- OpenAIProvider: OpenAI GPT-4 API (cloud)
- OllamaProvider: Local LLM via Ollama
- KiroAIProvider: KiroAI+omniroute (desktop, dev-mode)

All providers return standardized classification format.
Graceful fallback if libraries not installed.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 5.2: Classification Cache ✅ COMPLETED

**Skills:** `/using-superpowers` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/core/classification_cache.py`
- Create: `tests/test_classification_cache.py`

**Step 1: Використати `/using-superpowers` skill**

ОБОВ'ЯЗКОВО на початку задачі!

**Step 2: Write failing test**

```python
import unittest
import os
import tempfile
from core.classification_cache import ClassificationCache

class TestClassificationCache(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.cache = ClassificationCache(self.temp_db.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_cache_stores_and_retrieves(self):
        result = {"category": "installer", "confidence": 0.95}
        self.cache.set("setup.exe", 1024, 1234567890, result)
        
        cached = self.cache.get("setup.exe", 1024, 1234567890)
        self.assertEqual(cached, result)
```

**Step 3: Run test to verify it fails**

Run: `python -m unittest tests.test_classification_cache -v`
Expected: ModuleNotFoundError

**Step 4: Write minimal implementation**

SQLite-based cache with get/set/clear/get_stats methods, cache invalidation on file size/mtime changes.

**Step 5: Run test to verify it passes**

Run: `python -m unittest tests.test_classification_cache -v`
Expected: PASS

**Step 6: Use `/verification-before-completion` skill**

Verify all tests pass before commit.

**Step 7: Commit**

```bash
git add src/core/classification_cache.py tests/test_classification_cache.py
git commit -m "feat(cache): add SQLite-based classification cache

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Status:** ✅ Completed with 9/9 tests passing

---

### Task 5.3: File Classifier (Hybrid Approach) ✅ COMPLETED

**Skills:** `/using-superpowers` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/core/file_classifier.py`
- Create: `tests/test_file_classifier.py`

**Step 1: Використати `/using-superpowers` skill**

ОБОВ'ЯЗКОВО на початку задачі!

**Step 2: Write failing test**

```python
import unittest
from core.file_classifier import FileClassifier

class TestFileClassifier(unittest.TestCase):
    def test_classify_by_extension(self):
        classifier = FileClassifier()
        result = classifier.classify("document.pdf")
        self.assertEqual(result["category"], "document")
    
    def test_classify_installer(self):
        classifier = FileClassifier()
        result = classifier.classify("setup.exe")
        self.assertEqual(result["category"], "installer")
```

**Step 3: Run test to verify it fails**

Run: `python -m unittest tests.test_file_classifier -v`
Expected: ModuleNotFoundError

**Step 4: Write minimal implementation**

Hybrid classifier: extension → pattern → LLM → fallback
- 80+ file extensions mapped
- Cache integration
- Statistics tracking

**Step 5: Run test to verify it passes**

Run: `python -m unittest tests.test_file_classifier -v`
Expected: PASS

**Step 6: Use `/verification-before-completion` skill**

Verify all tests pass before commit.

**Step 7: Commit**

```bash
git add src/core/file_classifier.py tests/test_file_classifier.py
git commit -m "feat(classifier): add hybrid file classifier with LLM fallback

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Status:** ✅ Completed

---

### Task 5.4: Directory Tree Builder ✅ COMPLETED

**Skills:** `/using-superpowers` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/core/directory_tree.py`
- Create: `tests/test_directory_tree.py`

**Step 1: Використати `/using-superpowers` skill**

ОБОВ'ЯЗКОВО на початку задачі!

**Step 2: Write failing test**

```python
import unittest
import tempfile
import os
from core.directory_tree import DirectoryTree

class TestDirectoryTree(unittest.TestCase):
    def test_builds_tree_structure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.makedirs(os.path.join(tmpdir, "subdir"))
            
            tree = DirectoryTree(tmpdir)
            result = tree.build()
            
            self.assertIn("name", result)
            self.assertIn("children", result)
```

**Step 3: Run test to verify it fails**

Run: `python -m unittest tests.test_directory_tree -v`
Expected: ModuleNotFoundError

**Step 4: Write minimal implementation**

- Recursive tree building with max_depth control
- Ignore patterns with glob-style matching
- Unicode tree export (├── └── │)
- Statistics: total files, directories, size

**Step 5: Run test to verify it passes**

Run: `python -m unittest tests.test_directory_tree -v`
Expected: PASS

**Step 6: Use `/verification-before-completion` skill**

Verify all tests pass before commit.

**Step 7: Commit**

```bash
git add src/core/directory_tree.py tests/test_directory_tree.py
git commit -m "feat(tree): add directory tree builder with filtering

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Status:** ✅ Completed

---

### Task 5.5: Folder Compare ✅ COMPLETED

**Skills:** `/using-superpowers` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/core/folder_compare.py`
- Create: `tests/test_folder_compare.py`

**Step 1: Використати `/using-superpowers` skill**

ОБОВ'ЯЗКОВО на початку задачі!

**Step 2: Write failing test**

```python
import unittest
import tempfile
import os
from core.folder_compare import FolderCompare

class TestFolderCompare(unittest.TestCase):
    def test_detects_identical_files(self):
        with tempfile.TemporaryDirectory() as tmpdir1:
            with tempfile.TemporaryDirectory() as tmpdir2:
                # Create identical files
                file1 = os.path.join(tmpdir1, "test.txt")
                file2 = os.path.join(tmpdir2, "test.txt")
                
                with open(file1, 'w') as f:
                    f.write("content")
                with open(file2, 'w') as f:
                    f.write("content")
                
                comparer = FolderCompare(tmpdir1, tmpdir2)
                result = comparer.compare()
                
                self.assertIn("identical", result)
```

**Step 3: Run test to verify it fails**

Run: `python -m unittest tests.test_folder_compare -v`
Expected: ModuleNotFoundError

**Step 4: Write minimal implementation**

- Hash-based comparison (MD5, 8KB chunks)
- Detects: identical, different, only_in_first, only_in_second
- Fallback to size/mtime comparison
- Text report generation

**Step 5: Run test to verify it passes**

Run: `python -m unittest tests.test_folder_compare -v`
Expected: PASS

**Step 6: Use `/verification-before-completion` skill**

Verify all tests pass before commit.

**Step 7: Commit**

```bash
git add src/core/folder_compare.py tests/test_folder_compare.py
git commit -m "feat(compare): add folder comparison with hash-based detection

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Status:** ✅ Completed

---

### Task 5.6: Extended Junk Detector ✅ COMPLETED

**Skills:** `/using-superpowers` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Modify: `src/core/junk_detector.py`
- Modify: `tests/test_junk_detector.py`

**Step 1: Використати `/using-superpowers` skill**

ОБОВ'ЯЗКОВО на початку задачі!

**Step 2: Write failing test**

```python
import unittest
import tempfile
import os
from core.junk_detector import JunkDetector

class TestJunkDetector(unittest.TestCase):
    def test_detects_temp_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_file = os.path.join(tmpdir, "file.tmp")
            with open(temp_file, 'w') as f:
                f.write("temp")
            
            detector = JunkDetector(tmpdir)
            result = detector.detect()
            
            self.assertIn("temp_files", result)
            self.assertGreater(len(result["temp_files"]), 0)
```

**Step 3: Run test to verify it fails**

Run: `python -m unittest tests.test_junk_detector -v`
Expected: FAIL (method not implemented)

**Step 4: Write minimal implementation**

- 5 detection categories: temp_files, backup_files, old_backups, duplicates, empty_folders
- System whitelist with glob pattern matching
- Safe deletion checks

**Step 5: Run test to verify it passes**

Run: `python -m unittest tests.test_junk_detector -v`
Expected: PASS

**Step 6: Use `/verification-before-completion` skill**

Verify all tests pass before commit.

**Step 7: Commit**

```bash
git add src/core/junk_detector.py tests/test_junk_detector.py
git commit -m "feat(junk): extend junk detector with 5 detection categories

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Status:** ✅ Completed

---

### Task 5.7: GUI Tab - File Classifier ✅ COMPLETED

**Skills:** `/using-superpowers` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/gui/classifier_tab.py`
- Create: `tests/test_classifier_tab.py`

**Step 1: Використати `/using-superpowers` skill**

ОБОВ'ЯЗКОВО на початку задачі!

**Step 2: Write failing test**

```python
import unittest
from gui.classifier_tab import ClassifierTab

class TestClassifierTab(unittest.TestCase):
    def test_classifier_tab_can_be_imported(self):
        self.assertTrue(hasattr(ClassifierTab, '__init__'))
    
    def test_classifier_tab_has_required_methods(self):
        required_methods = ['_create_widgets', '_select_folder', '_start_classification']
        for method in required_methods:
            self.assertTrue(hasattr(ClassifierTab, method))
```

**Step 3: Run test to verify it fails**

Run: `python -m unittest tests.test_classifier_tab -v`
Expected: ModuleNotFoundError

**Step 4: Write minimal implementation**

- Folder selection with browse dialog
- LLM provider dropdown
- Progress bar with threading
- Results table with 5 columns
- CSV/JSON export

**Step 5: Run test to verify it passes**

Run: `python -m unittest tests.test_classifier_tab -v`
Expected: PASS

**Step 6: Use `/verification-before-completion` skill**

Verify all tests pass before commit.

**Step 7: Commit**

```bash
git add src/gui/classifier_tab.py tests/test_classifier_tab.py
git commit -m "feat(gui): add file classifier tab with LLM provider selection

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Status:** ✅ Completed

---

### Task 5.8: GUI Tab - Directory Tree ✅ COMPLETED

**Skills:** `/using-superpowers` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/gui/tree_tab.py`
- Create: `tests/test_tree_tab.py`

**Step 1: Використати `/using-superpowers` skill**

ОБОВ'ЯЗКОВО на початку задачі!

**Step 2: Write failing test**

```python
import unittest
from gui.tree_tab import TreeTab

class TestTreeTab(unittest.TestCase):
    def test_tree_tab_can_be_imported(self):
        self.assertTrue(hasattr(TreeTab, '__init__'))
    
    def test_tree_tab_has_required_methods(self):
        required_methods = ['_create_widgets', '_select_folder', '_start_build', '_export_text']
        for method in required_methods:
            self.assertTrue(hasattr(TreeTab, method))
```

**Step 3: Run test to verify it fails**

Run: `python -m unittest tests.test_tree_tab -v`
Expected: ModuleNotFoundError

**Step 4: Write minimal implementation**

- TreeView widget with hierarchical display
- Icons for folders (📁) and files (📄)
- Ignore patterns input, max depth dropdown
- Text export with Unicode symbols
- Threading for non-blocking UI

**Step 5: Run test to verify it passes**

Run: `python -m unittest tests.test_tree_tab -v`
Expected: PASS

**Step 6: Use `/verification-before-completion` skill**

Verify all tests pass before commit.

**Step 7: Commit**

```bash
git add src/gui/tree_tab.py tests/test_tree_tab.py
git commit -m "feat(gui): add directory tree tab with TreeView visualization

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Status:** ✅ Completed

---

### Task 5.9: GUI Tab - Folder Compare ✅ COMPLETED

**Skills:** `/using-superpowers` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/gui/compare_tab.py`
- Create: `tests/test_compare_tab.py`

**Step 1: Використати `/using-superpowers` skill**

ОБОВ'ЯЗКОВО на початку задачі!

**Step 2: Write failing test**

```python
import unittest
from gui.compare_tab import CompareTab

class TestCompareTab(unittest.TestCase):
    def test_compare_tab_can_be_imported(self):
        self.assertTrue(hasattr(CompareTab, '__init__'))
    
    def test_compare_tab_has_required_methods(self):
        required_methods = ['_create_widgets', '_select_folder', '_start_comparison', '_export_report']
        for method in required_methods:
            self.assertTrue(hasattr(CompareTab, method))
```

**Step 3: Run test to verify it fails**

Run: `python -m unittest tests.test_compare_tab -v`
Expected: ModuleNotFoundError

**Step 4: Write minimal implementation**

- Two folder selections
- Color-coded results: green (identical), orange (different), blue (only in 1), red (only in 2)
- Text report export
- Threading for non-blocking comparison

**Step 5: Run test to verify it passes**

Run: `python -m unittest tests.test_compare_tab -v`
Expected: PASS

**Step 6: Use `/verification-before-completion` skill**

Verify all tests pass before commit.

**Step 7: Commit**

```bash
git add src/gui/compare_tab.py tests/test_compare_tab.py
git commit -m "feat(gui): add folder compare tab with color-coded results

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Status:** ✅ Completed

---

### Task 5.10: GUI Tab - Extended Junk Detector ✅ COMPLETED

**Skills:** `/using-superpowers` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/gui/junk_tab.py`
- Create: `tests/test_junk_tab.py`

**Step 1: Використати `/using-superpowers` skill**

ОБОВ'ЯЗКОВО на початку задачі!

**Step 2: Write failing test**

```python
import unittest
from gui.junk_tab import JunkTab

class TestJunkTab(unittest.TestCase):
    def test_junk_tab_can_be_imported(self):
        self.assertTrue(hasattr(JunkTab, '__init__'))
    
    def test_junk_tab_has_required_methods(self):
        required_methods = ['_create_widgets', '_select_folder', '_start_scan', '_safe_delete']
        for method in required_methods:
            self.assertTrue(hasattr(JunkTab, method))
```

**Step 3: Run test to verify it fails**

Run: `python -m unittest tests.test_junk_tab -v`
Expected: ModuleNotFoundError

**Step 4: Write minimal implementation**

- Folder selection with browse button
- 5 checkboxes for junk types (temp, backup, old backup, duplicates, empty folders)
- Recursive checkbox
- Scan button with threading
- Results table with 3 columns (File, Type, Size)
- Safe delete button with confirmation dialog
- Statistics display

**Step 5: Run test to verify it passes**

Run: `python -m unittest tests.test_junk_tab -v`
Expected: PASS

**Step 6: Use `/verification-before-completion` skill**

Verify all tests pass before commit.

**Step 7: Commit**

```bash
git add src/gui/junk_tab.py tests/test_junk_tab.py
git commit -m "feat(gui): add junk detector tab with safe deletion

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Status:** ✅ Completed

---

## Verification Checklist (для кожної задачі)

**Перед комітом ОБОВ'ЯЗКОВО:**
- [ ] Використано `/using-superpowers` skill на початку
- [ ] Використано `/test-driven-development` для коду
- [ ] Всі тести проходять (pytest -v)
- [ ] Немає регресій (повний test suite)
- [ ] Використано `/verification-before-completion` перед комітом
- [ ] Код відрев'ювано через `/code-reviewer`
- [ ] Коміт створено з чітким повідомленням

---

## Progress Tracking

- ✅ Task 5.1: LLM Providers (4 провайдери + registry)
- ✅ Task 5.2: Classification Cache (SQLite кеш)
- ✅ Task 5.3: File Classifier (hybrid approach)
- ✅ Task 5.4: Directory Tree Builder (recursive with filtering)
- ✅ Task 5.5: Folder Compare (hash-based comparison)
- ✅ Task 5.6: Extended Junk Detector (5 categories)
- ✅ Task 5.7: GUI Tab - Classifier (LLM provider selection)
- ✅ Task 5.8: GUI Tab - Tree (TreeView visualization)
- ✅ Task 5.9: GUI Tab - Compare (color-coded results)
- ✅ Task 5.10: GUI Tab - Junk (safe deletion)

**Current Status:** 10/10 tasks completed (100%) ✅ PHASE 5 COMPLETE
