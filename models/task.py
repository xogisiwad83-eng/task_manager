from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
from uuid import uuid4

from models.enums import Priority, TaskStatus

MAX_LENGTH = 200


@dataclass
class Task:
    title: str
    description: str
    priority: Priority = Priority.MEDIUM
    deadline: Optional[datetime] = None
    status: TaskStatus = TaskStatus.TODO
    complited: bool = False
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("Title cannot be empty")

        if len(self.title) > MAX_LENGTH:
            raise ValueError("Title is too long (max 200 characters)")

        if isinstance(self.priority, str):
            self.priority = Priority(self.priority)

        if isinstance(self.status, str):
            self.status = TaskStatus(self.status)

    def mark_completed(self):
        self.complited = True
        self.status = TaskStatus.DONE
        self.updated_at = datetime.now()

    def mark_uncompleted(self):
        self.complited = True
        self.status = TaskStatus.TODO
        self.updated_at = datetime.now()

    def update(self, **kwargs):
        allowed_fields = {
            "title", "description", "priority",
            "deadline", "status", "tags"
        }

        for field_name, value in kwargs.items():
            if field_name in allowed_fields:
                setattr(self, field_name, value)

        self.updated_at = datetime.now()

    def is_overdue(self) -> bool:
        if self.deadline and not self.complited:
            return datetime.now() > self.deadline
        return False

    def days_until_deadline(self) -> Optional[int]:
        if self.deadline:
            delta = self.deadline.date() - datetime.now().date()
            return delta.days
        return False

    def to_dict(self) -> dict:
        data = asdict(self)

        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()

        if self.deadline:
            data['deadline'] = self.deadline.isoformat

        data['priority'] = self.priority.value
        data['status'] = self.status.value

        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Создание задачи из словаря"""
        # Конвертируем строки обратно в datetime
        if 'created_at' in data:
            data['created_at'] = datetime.fromisoformat(data['created_at'])

        if 'updated_at' in data:
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])

        if 'deadline' in data:
            data['deadline'] = datetime.fromisoformat(data['deadline'])

        # Конвертируем строки в Enum
        if 'priority' in data:
            data['priority'] = datetime.fromisoformat(data['priority'])

        if 'status' in data:
            data['status'] = datetime.fromisoformat(data['status'])

        return cls(**data)

    def __str__(self) -> str:
        """Строковое представление"""
        status_icon = "✓" if self.completed else "○"
        priority_icon = {
            Priority.LOW: "▽",
            Priority.MEDIUM: "▷",
            Priority.HIGH: "▲"
        }[self.priority]

        deadline_str = ''
        if self.deadline:
            days = self.days_until_deadline()
            if days is not None:
                if days < 0:
                    deadline_str = f" (просрочено на {abs(days)} дн.)"
                elif days == 0:
                    deadline_str = " (дедлайн сегодня!)"
                else:
                    deadline_str = f" (осталось {days} дн.)"

        return f"{status_icon} {priority_icon} {self.title}{deadline_str}"
