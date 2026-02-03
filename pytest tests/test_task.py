import pytest

from datetime import datetime, timedelta
from models.task import Task
from models.enums import Priority, TaskStatus

def test_task_creation():
    pass

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
    future_deadline = datetime.now() + timedelta(days=1)
    task_past = Task(title= "Past",deadline=past_deadline)
    task_future = Task(title= "Future",deadline=future_deadline)

    assert task_past is True
    assert task_future is False

def test_task_update():
    pass

def test_task_serialization():
    pass