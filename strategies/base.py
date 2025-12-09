from abc import ABC, abstractmethod
from models.task import Task


class PriorityStrategy(ABC):
    """Абстракная стратегия расчёта приоритета"""

    @abstractmethod
    def calculate_priority(self, task: Task) -> float:
        """
        Рассчитать числовой проритет задачи

        Чем выше число, тем выше приоритет

        Returns:
            float: Числовой приоритет
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Название стратегии"""
        pass
