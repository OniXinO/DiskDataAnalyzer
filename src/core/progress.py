"""
Прогрес-бар для CLI
"""

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


class ProgressBar:
    """Прогрес-бар з підтримкою tqdm"""

    def __init__(self, total, desc="Progress"):
        """
        Ініціалізація прогрес-бару

        Args:
            total: Загальна кількість елементів
            desc: Опис прогресу
        """
        self.total = total
        self.current = 0
        self.desc = desc

        if TQDM_AVAILABLE:
            self.pbar = tqdm(total=total, desc=desc, unit="items")
        else:
            self.pbar = None

    def update(self, n=1):
        """
        Оновити прогрес

        Args:
            n: Кількість елементів для додавання
        """
        self.current += n
        if self.current > self.total:
            self.current = self.total

        if self.pbar:
            self.pbar.update(n)

    def close(self):
        """Закрити прогрес-бар"""
        if self.pbar:
            self.pbar.close()
