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

**Implementation:** SQLite-based cache with get/set/clear/get_stats methods, cache invalidation on file size/mtime changes.

**Status:** ✅ Completed with 9/9 tests passing

---

### Task 5.3: File Classifier (Hybrid Approach)

**Skills:** `/using-superpowers` → `/test-driven-development` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/core/file_classifier.py`
- Create: `tests/test_file_classifier.py`

**Approach:**
1. Pattern matching (90%): швидка класифікація за назвою/розширенням
2. LLM fallback (10%): складні випадки через LLM провайдер
3. Cache integration: перевірка кешу перед LLM викликом

---

### Task 5.4: Directory Tree Builder

**Skills:** `/using-superpowers` → `/test-driven-development` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/core/directory_tree.py`
- Create: `tests/test_directory_tree.py`

**Features:**
- Рекурсивна побудова дерева каталогів
- Підтримка фільтрації (ignore patterns)
- Експорт в текстовий формат
- Статистика (кількість файлів/папок, загальний розмір)

---

### Task 5.5: Folder Compare

**Skills:** `/using-superpowers` → `/test-driven-development` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/core/folder_compare.py`
- Create: `tests/test_folder_compare.py`

**Features:**
- Порівняння двох папок за структурою
- Виявлення відмінностей (нові/видалені/змінені файли)
- Порівняння за hash для виявлення ідентичних файлів
- Звіт про відмінності

---

### Task 5.6: Extended Junk Detector

**Skills:** `/using-superpowers` → `/test-driven-development` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Modify: `src/core/junk_detector.py`
- Modify: `tests/test_junk_detector.py`

**New Features:**
- Виявлення залишкових файлів після деінсталяції
- Пошук порожніх папок
- Виявлення застарілих backup файлів
- Пошук дублікатів за hash
- Безпечність видалення (whitelist системних файлів)

---

### Task 5.7: GUI Tab - File Classifier

**Skills:** `/using-superpowers` → `/test-driven-development` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/gui/classifier_tab.py`
- Create: `tests/test_classifier_tab.py`

**Features:**
- Вибір папки для класифікації
- Вибір LLM провайдера
- Прогрес-бар
- Таблиця результатів з категоріями
- Експорт результатів

---

### Task 5.8: GUI Tab - Directory Tree

**Skills:** `/using-superpowers` → `/test-driven-development` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/gui/tree_tab.py`
- Create: `tests/test_tree_tab.py`

**Features:**
- Вибір папки
- Візуалізація дерева (TreeView widget)
- Фільтри (ignore patterns)
- Експорт в текст
- Статистика

---

### Task 5.9: GUI Tab - Folder Compare

**Skills:** `/using-superpowers` → `/test-driven-development` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/gui/compare_tab.py`
- Create: `tests/test_compare_tab.py`

**Features:**
- Вибір двох папок
- Кнопка "Compare"
- Таблиця відмінностей (нові/видалені/змінені)
- Кольорове виділення
- Експорт звіту

---

### Task 5.10: GUI Tab - Extended Junk Detector

**Skills:** `/using-superpowers` → `/test-driven-development` → test-engineer → feature-implementer → code-reviewer → verification-before-completion

**Files:**
- Create: `src/gui/junk_tab.py`
- Create: `tests/test_junk_tab.py`

**Features:**
- Вибір папки для сканування
- Чекбокси для типів сміття (temp files, duplicates, empty folders, etc.)
- Прогрес-бар
- Таблиця знайденого сміття з розміром
- Кнопка "Safe Delete" (з підтвердженням)
- Статистика звільненого місця

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
- ⏳ Task 5.3: File Classifier (наступна)
- ⏳ Task 5.4: Directory Tree Builder
- ⏳ Task 5.5: Folder Compare
- ⏳ Task 5.6: Extended Junk Detector
- ⏳ Task 5.7: GUI Tab - Classifier
- ⏳ Task 5.8: GUI Tab - Tree
- ⏳ Task 5.9: GUI Tab - Compare
- ⏳ Task 5.10: GUI Tab - Junk

**Current Status:** 2/10 tasks completed (20%)
