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
        """
        Зареєструвати новий провайдер

        Args:
            name: Унікальне ім'я провайдера (наприклад "claude", "openai")
            provider_class: Клас провайдера (наслідує LLMProvider)

        Raises:
            TypeError: Якщо provider_class не наслідує LLMProvider

        Example:
            LLMRegistry.register("custom_llm", CustomLLMProvider)
        """
        if not issubclass(provider_class, LLMProvider):
            raise TypeError(f"{provider_class} must inherit from LLMProvider")

        if name in cls._providers:
            logger.warning(f"Provider '{name}' already registered, overwriting")

        cls._providers[name] = provider_class
        logger.info(f"Registered LLM provider: {name}")

    @classmethod
    def get_provider(cls, name: str, **kwargs) -> LLMProvider:
        """
        Отримати екземпляр провайдера

        Args:
            name: Ім'я провайдера
            **kwargs: Аргументи для конструктора провайдера

        Returns:
            LLMProvider: Екземпляр провайдера

        Raises:
            KeyError: Якщо провайдер не зареєстровано

        Example:
            provider = LLMRegistry.get_provider("claude", api_key="...")
        """
        if name not in cls._providers:
            available = cls.list_providers()
            raise KeyError(f"Provider '{name}' not registered. Available: {available}")

        provider_class = cls._providers[name]
        return provider_class(**kwargs)

    @classmethod
    def list_providers(cls) -> List[str]:
        """Отримати список зареєстрованих провайдерів"""
        return list(cls._providers.keys())

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Перевірити чи провайдер зареєстровано"""
        return name in cls._providers

    @classmethod
    def unregister(cls, name: str):
        """Видалити провайдер з реєстру"""
        if name in cls._providers:
            del cls._providers[name]
            logger.info(f"Unregistered LLM provider: {name}")


# Автоматична реєстрація вбудованих провайдерів
def _register_builtin_providers():
    """Зареєструвати вбудовані провайдери"""
    from core.llm_providers import (
        ClaudeProvider, OpenAIProvider,
        OllamaProvider, KiroAIProvider,
        ANTHROPIC_AVAILABLE, OPENAI_AVAILABLE,
        OLLAMA_AVAILABLE, REQUESTS_AVAILABLE
    )

    if ANTHROPIC_AVAILABLE:
        LLMRegistry.register("claude", ClaudeProvider)

    if OPENAI_AVAILABLE:
        LLMRegistry.register("openai", OpenAIProvider)

    if OLLAMA_AVAILABLE:
        LLMRegistry.register("ollama", OllamaProvider)

    if REQUESTS_AVAILABLE:
        LLMRegistry.register("kiroai", KiroAIProvider)


# Реєструємо при імпорті модуля
_register_builtin_providers()
