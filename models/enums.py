from enum import Enum


class Priority(str, Enum):
    """Приоритет задачи"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    def __str__(self):
        return self.value

    @property
    def numeric_value(self):
        mapping = {
            Priority.LOW: 1,
            Priority.MEDIUM: 2,
            Priority.HIGH: 3
        }
        return mapping[self]


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in progress"
    DONE = "done"
    CANCELLED = "cancelled"

    def __str__(self):
        return self.value
