from typing import List, Dict

from storage.base import Storage
from models.task import Task
from observers.base import Observer
from datetime import datetime
from pathlib import Path

from storage.csv_storage import CSVStorage
from storage.json_storage import JSONStorage


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
        """
                Добавляет новую задачу.

                Args:
                    task (Task): Объект задачи

                Returns:
                    bool: True если задача добавлена успешно, иначе False
                """
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
        """
                Удаляет задачу по идентификатору.

                Args:
                    task_id (str): Идентификатор задачи

                Returns:
                    bool: True при успешном удалении, иначе False
                """
        try:
            task = self.get_task(task_id)

            self.tasks.remove(task)
            self._add_to_history("deleted", task)
            self.tasks.remove(task)
            self.notify_observers('task_deleted', {
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
        """
                Добавляет запись в историю изменений.

                Args:
                    action (str): Тип действия (created, updated, deleted и т.д.)
                    task (Task): Задача, над которой выполнено действие
                    old_state (dict, optional): Предыдущее состояние задачи
                """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'task_id': task.id,
            'task_title': task.title
        }
        if action == 'updated' and old_state:
            entry['old_state'] = old_state
            entry['new_state'] = task.to_dict()
        self.history.append(entry)

    def save_tasks(self):
        """
        Сохраняет текущие задачи в хранилище.

        Returns:
            bool: True при успешном сохранении
        """
        try:
            self.storage.save(self.tasks)
            self.notify_observers("tasks_saved", {})
            return True
        except Exception as e:
            self.notify_observer("error", {"message": str(e)})
            return False

    def get_task(self, task_id: str):
        """
                Получает задачу по идентификатору.

                Args:
                    task_id (str): Идентификатор задачи

                Returns:
                    Task | None: Найденная задача или None
                """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

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
        results = []
        for task in self.tasks:
            if query_lower in task.title.lower() or query_lower in task.description.lower():
                results.append(task)
        return results

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
        return [task for task in self.tasks if filter_func(task)]

    def sort_tasks(self, tasks = None, strategy = None , reverse = True):
        """
            Сортировка задач с использованием стратегии или по дате создания

            Args:
                tasks: Список задач для сортировки (если None — все задачи)
                strategy: Стратегия приоритизации (опционально)
                reverse: Направление сортировки

            Returns:
                List[Task]: Отсортированные задачи
            """
        tasks_to_sort = tasks if tasks is not None else self.tasks

        if strategy:
            return sorted(
                tasks_to_sort,
                key=lambda task: strategy.calculate_priority(task),
                reverse=reverse
            )



    def update_task(self, task_id: str, **kwargs) -> bool:
        """
           Обновляет параметры задачи.

           Args:
               task_id (str): Идентификатор задачи
               **kwargs: Поля задачи и их новые значения

           Returns:
               bool: True если задача успешно обновлена, иначе False
           """
        task = self.get_task(task_id)

        if not task:
            return False

        try:
            old_state = task.to_dict()
            task.update(**kwargs)
            self._add_to_history('updated', task, old_state)
            self.save_tasks()
            self.notify_observer('task_updated', {
                'id': task_id,
                'title': task.title,
                'changes': kwargs
            })
            return True
        except Exception as e:
            self.notify_observer('error', {'message': str(e)})
            return False

    def complete_task(self, task_id: str) -> bool:
        """
           Отмечает задачу как выполненную.

           Args:
               task_id (str): Идентификатор задачи

           Returns:
               bool: True если задача успешно завершена, иначе False
           """
        task = self.get_task(task_id)

        if not task:
            return False

        task.mark_completed()
        self._add_to_history('completed', task)
        self.save_tasks()
        self.notify_observer('task_completed', {
            'id': task_id,
            'title': task.title
        })
        return True

    def get_statistics(self) -> dict:
        """
            Возвращает статистику по задачам.

            Включает:
            - общее количество задач
            - количество выполненных и невыполненных
            - количество просроченных
            - процент выполнения
            - распределение по приоритетам и статусам

            Returns:
                dict: Статистическая информация по задачам
            """
        total = len(self.tasks)
        completed = len(self.get_completed_tasks())
        uncompleted = total - completed
        overdue = len(self.get_overdue_tasks())
        return {
            "total": total,
            "completed": completed,
            "uncompleted": uncompleted,
            "overdue": overdue,
            "competion_percent": (completed/total*100) if total else  0,
            "by_priority": {
                "high":(self.get_tasks_by_priority("high")),
                "medium":(self.get_tasks_by_priority("medium")),
                "low":(self.get_tasks_by_priority("low"))
            },
            "by_status": {
                status: len(self.get_tasks_by_status(status))
                for status in ["todo", "in_progress", "done", "cancelled"]
            }
        }

    def load_task(self):
        """
           Загружает задачи из хранилища.

           Перезаписывает текущий список задач и уведомляет наблюдателей.

           Returns:
               bool: True при успешной загрузке, иначе False
           """
        try:
            self.tasks = self.storage.load()
            self.notify_observer("task_loaded", {
                "count": len(self.tasks)
            })
            return True
        except Exception as e:
            self.notify_observer('error', {'message': str(e)})
            return False

    def export_tasks(self, format: str, path: Path):
        """
           Экспортирует задачи в файл указанного формата.

           Поддерживаемые форматы:
           - json
           - csv

           Args:
               format (str): Формат экспорта ('json' или 'csv')
               path (Path): Путь к файлу экспорта

           Returns:
               bool: True при успешном экспорте, иначе False
           """
        try:
            if format == "json":
                storage = JSONStorage(path)
            elif format == "csv":
                storage = CSVStorage(path)
            else:
                raise ValueError(f"Неизвестный формат {format}")
            return storage.export(self.tasks, path)
        except Exception as e:
            self.notify_observer('error', {'message': str(e)})
            return False

    def get_history(self, limit: int = 50) -> list[dict]:
        """
            Возвращает историю действий над задачами.

            Args:
                limit (int): Максимальное количество записей

            Returns:
                list[dict]: Список записей истории
            """
        return self.history[-limit:]

    def clear_history(self):
        """
           Полностью очищает историю изменений задач.
           """
        self.history.clear()

