from abc import ABC, abstractmethod
from typing import List
from pathlib import Path
from models.task import Task

class Storage(ABC):
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file_path.parents.mkdir(parents = True)

    @ abstractmethod

    def save(self, tasks: List[Task]) -> bool
        pass
    """Абстрактный
    метод
    для
    сохранения."""

    @abstractmethod

    def load(self) -> List[Task]:
        """Абстрактный метод для загрузки"""

        pass

    @abstractmethod

    def export(self, tasks: List[Task], export_path: Path) -> bool:

    """Абстрактный метод для экспорта"""

        pass


