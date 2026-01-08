import logging
from calendar import error

from observers.base import Observer
from datetime import datetime
from pathlib import Path
from typing import Any


class LoggerObserver(Observer):
    """Наблюдатель, который логирует все собития"""

    def __init__(self, log_file: Path):
        """
        Args:
            log_file: Путь к файлу логов
        """
        self.log_file = log_file

    def setup_logger(self):
        self.logger = logging.getLogger("TaskManager")
        self.logger.setLevel(logging.INFO)

        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def update(self, event: str, data: Any):
        """Логирование событий"""
        if event == "task_added":
            self.logger.info(f"Task added: {data['title']}")

        elif event == 'task_updated':
            self.logger.info(f'Task Updated: {data['title']}')

        elif event == 'task_deleted':
            self.logger.info(f'Task Deleted: {data['title']}')

        elif event == 'task_completed':
            self.logger.info(f'Task Completed: {data['title']}')

        elif event == 'task_loaded':
            self.logger.info(f'Loaded {data['count']} tasks')

        elif event == 'task_saved':
            self.logger.info(f'Saved {data['count']} tasks')
        elif event == 'error':
            self.logger.error(f'Error: {data['message']}')

        else:
            self.logger.info(f'Event {event}: {data}')

