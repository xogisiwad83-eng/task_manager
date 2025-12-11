from abc import ABC, abstractmethod
from typing import Any


class Observer(ABC):
    """Абстрактный наблюдатель"""

    @abstractmethod
    def update(self, event: str, data: Any):
        """
        Получение уведомлений о событии

        Args:
            event: Тип события ('Task_added', 'task_updated' и т.д.)
            data: Данные события
        """
        pass
