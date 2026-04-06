"""
Тести для LLM Registry
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.llm_registry import LLMRegistry
from core.llm_providers import LLMProvider


class MockLLMProvider(LLMProvider):
    """Mock провайдер для тестування"""
    def __init__(self, test_param="default"):
        self.test_param = test_param

    def classify_file(self, filename, context):
        return {
            "category": "test",
            "description_uk": "Тестовий файл",
            "confidence": 1.0
        }


class TestLLMRegistry(unittest.TestCase):
    """Тести для реєстру LLM провайдерів"""

    def test_register_provider(self):
        """Тест реєстрації провайдера"""
        LLMRegistry.register("mock_test", MockLLMProvider)
        self.assertTrue(LLMRegistry.is_registered("mock_test"))

    def test_get_provider_returns_instance(self):
        """Тест що get_provider повертає екземпляр"""
        LLMRegistry.register("mock_test2", MockLLMProvider)
        provider = LLMRegistry.get_provider("mock_test2", test_param="custom")

        self.assertIsInstance(provider, MockLLMProvider)
        self.assertEqual(provider.test_param, "custom")

    def test_list_providers_returns_list(self):
        """Тест що list_providers повертає список"""
        providers = LLMRegistry.list_providers()
        self.assertIsInstance(providers, list)

    def test_get_nonexistent_provider_raises_error(self):
        """Тест що неіснуючий провайдер викликає помилку"""
        with self.assertRaises(KeyError):
            LLMRegistry.get_provider("nonexistent_provider_xyz")

    def test_register_non_provider_class_raises_error(self):
        """Тест що реєстрація не-провайдера викликає помилку"""
        class NotAProvider:
            pass

        with self.assertRaises(TypeError):
            LLMRegistry.register("invalid", NotAProvider)


if __name__ == '__main__':
    unittest.main()
