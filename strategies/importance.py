from strategies.base import PriorityStrategy
from models.task import Task


class ImportancePriorityStrategy(PriorityStrategy):
    """
    Приоритизация только по установленному приоритету
    
    Игнорирует дедлайны, сортирует только по Priority
    """
    
    def calculate_priority(self, task: Task) -> float:
        """Просто возвращаем числовое значение приоритета"""
        return task.priority.numeric_value
    
    def get_name(self) -> str:
        return "Importance Priority"