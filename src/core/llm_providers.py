"""
LLM провайдери для класифікації файлів
Підтримує: Claude API, OpenAI API, Ollama (локальний), KiroAI+omniroute (dev)
"""

from abc import ABC, abstractmethod
import json
import logging

logger = logging.getLogger(__name__)

# Перевірка доступності бібліотек
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

            # Ollama може повертати текст з markdown
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
