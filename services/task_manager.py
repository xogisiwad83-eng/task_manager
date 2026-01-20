from typing import List, Dict

from storage.base import Storage
from models.task import Task
from observers.base import Observer


class TaskManager:
    """
    Основной менеджер задач, реализующий паттерн
    Наблюдатель. Управляет задачами и уведомлениями наблюдателей.
    """

    def __init__(self, storage: Storage):
        """
        Инициализировать TaskManager.

        Аргументы:
        storage (Storage): Экземпляр Storage для сохранения задач.
        """
        self.storage: Storage = storage
        self.tasks: List[Task] = []
        self.observers: List[Observer] = []
        self.history: List[Dict] = []

        self._load_tasks()

    def _load_tasks(self) -> None:
        """Загрузить существующие задачи из хранилища."""
        try:
            self.tasks = self.storage.load()
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []

    def add_observer(self, observer: Observer) -> None:
        """
        Добавить наблюдателя.

        Аргументы:
        observer (Observer): экземпляр наблюдателя.
        """
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        """
        Удалить наблюдателя.

        Аргументы:
        observer (Observer): экземпляр наблюдателя.
        """
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, event: str, data: dict) -> None:
        """
        Уведомьте наблюдателей о событии.

        Аргументы:
        event (str): Название события.
        data (dict): Данные события.
        """
        for observer in self.observers:
            try:
                observer.update(event, data)
            except Exception as e:
                print(f"Observer error: {e}")

    def add_task(self, task: Task) -> bool:
        try:
            self.tasks.append(task)
            self._add_to_history("created", task)
            self.save_tasks()
            self.notify_observer('task_added', {
                'id': task.id,
                'title': task.title
            })
            return True
        except Exception as e:
            self.notify_observer('error', {
                'message': str(e)
            })
            return False

    def delete_task(self, task_id: str):
        try:
            task = self.get_task

            self.tasks.remove(task)
            self._add_to_history("created", task)
            self.save_tasks()
            self.notify_observer('task_added', {
                'id': task.id,
                'title': task.title
            })
            return True
        except Exception as e:
            self.notify_observer('error', {
                'message': str(e)
            })
            return False


    def _add_to_history(self, action: str, task: Task, old_state: dict = None):
        pass

    def save_tasks(self):
        try:
            self.storage.save(self.tasks)
            self.notify_observers("tasks_saved", {})
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def get_task(self):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def notify_observer(self, event: str, data: dict):
        for observer in self.observers:
            observer.update(event, data)

    def get_all_tasks(self) -> List[Task]:
        """Получить все задачи"""
        return self.tasks.copy()

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Получить задачи по статусу"""
        return [task for task in self.tasks if task.status == status]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Получить задачи по приоритету"""
        return [task for task in self.tasks if task.priority == priority]

    def get_completed_tasks(self) -> List[Task]:
        """Получить завершённые задачи"""
        return [task for task in self.tasks if task.complited]

    def get_incomplete_tasks(self) -> List[Task]:
        """Получить незавершённые задачи"""
        return [task for task in self.tasks if not task.complited]

    def get_overdue_tasks(self) -> List[Task]:
        """Получить просроченные задачи"""
        return [task for task in self.tasks if task.is_overdue()]

    def get_tasks_by_tag(self, tag: str) -> List[Task]:
        """Получить задачи по тегу"""
        return [task for task in self.tasks if tag in task.tags ]

    def search_tasks(self, query: str) -> List[Task]:
        """
        Поиск задач по названию или описанию

        Args:
            query: Поисковый запрос

        Returns:
            List[Task]: Найденные задачи
        """
        query_lower = query.lower()
        for task in self.tasks:
            if query_lower in task.title.lower() or query_lower in task.description.lower():

    def filter_tasks(self, filter_func: Callable[[Task], bool]) -> List[Task]:
        """
        Универсальная фильтрация задач

        Args:
            filter_func: Функция-фильтр

        Example:
            # Задачи с дедлайном на этой неделе
            manager.filter_tasks(lambda t: t.days_until_deadline() <= 7)

        Returns:
            List[Task]: Отфильтрованные задачи
        """
