from datetime import datetime
from strategies.base import PriorityStrategy
from models.task import Task

class CombinedPriorityStrategy(PriorityStrategy):
    """
    Комбинированная стратегия
    
    Учитывает:
    - Приоритет задачи
    - Дедлайн
    - Статус выполнения
    - Время с момента создания
    """
    
    def calculate_priority(self, task: Task) -> float:
        """Комплексный расчёт приоритета"""
        score = 0.0
        
        # 1. Базовый приоритет (0-300)
        score += task.priority.numeric_value * 100
        
        # 2. Дедлайн (0-500)
        if task.deadline:
            days_until = task.days_until_deadline()
            if days_until is not None:
                if days_until < 0:
                    score += 500  # Просрочено
                elif days_until == 0:
                    score += 400  # Сегодня
                elif days_until <= 3:
                    score += 300  # Эта неделя
                elif days_until <= 7:
                    score += 200
                else:
                    score += 100
        
        # 3. Возраст задачи (0-100)
        # Старые невыполненные задачи важнее
        age_days = (datetime.now() - task.created_at).days
        if not task.completed and age_days > 7:
            score += min(age_days * 2, 100)
        
        # 4. Статус (бонус за задачи в работе)
        if task.status.value == "in_progress":
            score += 50
        
        return score
    
    def get_name(self) -> str:
        return "Combined Priority"