"""
Тести для LLM провайдерів
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.llm_providers import (
    LLMProvider, ClaudeProvider, OpenAIProvider, OllamaProvider, KiroAIProvider,
    ANTHROPIC_AVAILABLE, OPENAI_AVAILABLE, OLLAMA_AVAILABLE, REQUESTS_AVAILABLE
)


class TestLLMProviders(unittest.TestCase):
    """Тести для LLM провайдерів"""

    @unittest.skipUnless(ANTHROPIC_AVAILABLE, "anthropic not installed")
    def test_claude_provider_has_classify_method(self):
        """Тест що Claude provider має метод classify_file"""
        provider = ClaudeProvider(api_key="test_key")
        self.assertTrue(hasattr(provider, 'classify_file'))
        self.assertTrue(callable(provider.classify_file))

    @unittest.skipUnless(OPENAI_AVAILABLE, "openai not installed")
    def test_openai_provider_has_classify_method(self):
        """Тест що OpenAI provider має метод classify_file"""
        provider = OpenAIProvider(api_key="test_key")
        self.assertTrue(hasattr(provider, 'classify_file'))
        self.assertTrue(callable(provider.classify_file))

    @unittest.skipUnless(OLLAMA_AVAILABLE, "ollama not installed")
    def test_ollama_provider_has_classify_method(self):
        """Тест що Ollama provider має метод classify_file"""
        provider = OllamaProvider()
        self.assertTrue(hasattr(provider, 'classify_file'))
        self.assertTrue(callable(provider.classify_file))

    @unittest.skipUnless(REQUESTS_AVAILABLE, "requests not installed")
    def test_kiroai_provider_has_classify_method(self):
        """Тест що KiroAI provider має метод classify_file"""
        provider = KiroAIProvider(base_url="http://localhost:8080")
        self.assertTrue(hasattr(provider, 'classify_file'))
        self.assertTrue(callable(provider.classify_file))

    def test_provider_returns_valid_structure(self):
        """Тест що provider повертає правильну структуру даних"""
        # Mock provider для тестування структури
        class MockProvider(LLMProvider):
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
        self.assertIsInstance(result["confidence"], (int, float))


if __name__ == '__main__':
    unittest.main()
