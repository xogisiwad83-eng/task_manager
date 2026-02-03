import pytest

from datetime import datetime, timedelta
from models.task import Task
from models.enums import Priority, TaskStatus

def test_task_creation():
    task = Task(title="",description="",priority=Priority.MEDIUM)
    assert task.title == ""
    assert task.description == ""
    assert task.priority == Priority.MEDIUM
    assert task.id is not None
    assert task.completed is False

def test_task_validation_empty_title():
    with pytest.raises(ValueError):
        Task(title="")


def test_task_validation_long_title():
    with pytest.raises(ValueError):
        Task(title="a" * 201)

def test_task_completion():
    task = Task(title ="Test")

    task.mark_completed()
    assert task.completed is True
    assert task.status == TaskStatus.DONE

def test_task_overdue():
    past_deadline = datetime.now() - timedelta(days=1)
    task_past = Task(title="Past", deadline=past_deadline)
    assert task_past is True

    future_deadline = datetime.now() + timedelta(days=1)
    task_future = Task(title="Future",deadline=future_deadline)
    assert task_future is False

def test_task_update():
    task =  Task(title="", description="", priority=Priority.MEDIUM)
    task.update(title="  ")
    assert task.title == "   "
    assert task.description == ""
    assert task.priority == Priority.MEDIUM

def test_task_serialization():
    task = Task(title="", description="", priority=Priority.MEDIUM, tags=["optimus", "lana rouds"])
    data = task.to_dict()
    restored = task.from_dict(data)
    assert restored.title == task.title
    assert restored.description == task.description
    assert restored.priority == task.priority
    assert restored.tags == task.tags
