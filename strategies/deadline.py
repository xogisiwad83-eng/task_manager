from strategies.base import PriorityStrategy
from models.task import Task


class DeadlinePriorityStrategy(PriorityStrategy):
    """
    Приоритезация по дедлайну

    Чем ближе дедлайн, тем выше приоритет
    """

    def calculate_priority(self, task: Task) -> float:
        """
        Расчёт приоритета на основе дедлайна

        Логика:
            - Нет дедлайна: базовый приоритет (100-300)
            - Есть дедлайн: базовый приоритет + бонус за близость
        """
        # Базовый приоритет
        base_priority = task.priority.numeric_value * 100

        # Если нет дедлайна, возвращаем базовый
        if not task.deadline:
            return base_priority

        # Рассчитываем дни до дедлайна
        days_until = task.days_until_deadline()

        if days_until is None:
            return base_priority

        # Бонус за близость дедлайна
        if days_until < 0:
            # Просроченно - максимальный приоритет
            bonus = 1000 + abs(days_until)
        elif days_until == 0:
            # Сегодня - очень высокий приоритет
            bonus = 500
        elif days_until <= 3:
            # Близкий дедлайн
            bonus = 300 / days_until
        elif days_until <= 7:
            # В течении недели
            bonus = 100 / days_until
        else:
            # Дальний дедлайн
            bonus = 50 / days_until

        return base_priority + bonus

    def get_name(self) -> str:
        return "Deadline Priority"
