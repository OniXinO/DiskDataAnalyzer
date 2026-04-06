"""
Кольоровий вивід для CLI
"""

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


class Colors:
    """Кольори для CLI"""
    if COLORAMA_AVAILABLE:
        RED = Fore.RED
        GREEN = Fore.GREEN
        YELLOW = Fore.YELLOW
        BLUE = Fore.BLUE
        MAGENTA = Fore.MAGENTA
        CYAN = Fore.CYAN
        WHITE = Fore.WHITE
        RESET = Style.RESET_ALL
    else:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""


def colorize(text, color):
    """
    Додати колір до тексту

    Args:
        text: Текст для кольорування
        color: Колір з Colors

    Returns:
        str: Кольоровий текст
    """
    if COLORAMA_AVAILABLE:
        return f"{color}{text}{Style.RESET_ALL}"
    return text


def success(text):
    """Повідомлення про успіх (зелений)"""
    return colorize(f"✅ {text}", Colors.GREEN)


def error(text):
    """Повідомлення про помилку (червоний)"""
    return colorize(f"❌ {text}", Colors.RED)


def warning(text):
    """Попередження (жовтий)"""
    return colorize(f"⚠️  {text}", Colors.YELLOW)


def info(text):
    """Інформація (синій)"""
    return colorize(f"ℹ️  {text}", Colors.BLUE)
