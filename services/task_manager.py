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