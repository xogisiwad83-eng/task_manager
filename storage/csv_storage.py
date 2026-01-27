import csv
from typing import List
from pathlib import Path
from storage.base import Storage
from models.task import Task


class CSVStorage(Storage):
    """Экспорт задач в CSV формате"""

    def save(self, tasks: List[Task]) -> bool:
        """CSV используется только для экспорта, не для основного хранения"""
        return self.export(tasks, self.file_path)

    def load(self) -> List[Task]:
        """Загрузка из CSV не поддерживается в текущей версии"""
        return []

    def export(self, tasks: List[Task], export_path: Path) -> bool:
        """
        Экспорт задач в CSV-файл.

        Аргументы:
        tasks (List[Task]): Список задач для экспорта.
        export_path (Path): Путь к CSV-файлу.

        Возвращает:
        bool: True, если экспорт прошел успешно, False в противном случае.
        """
        try:
            export_path.parent.mkdir(parents=True, exist_ok=True)

            fieldnames = [
                "id",
                "title",
                "description",
                "priority",
                "status",
                "completed",
                "deadline",
                "created_at",
                "updated_at",
                "tags",
            ]

            with export_path.open("w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for task in tasks:
                    writer.writerow({
                        "id": task.id,
                        "title": task.title,
                        "description": task.description or "",
                        "priority": task.priority.name if task.priority else "",
                        "status": task.status.name if task.status else "",
                        "completed": task.completed,
                        "deadline": task.deadline.isoformat() if task.deadline else "",
                        "created_at": task.created_at.isoformat() if task.created_at else "",
                        "updated_at": task.updated_at.isoformat() if task.updated_at else "",
                        "tags": ",".join(task.tags) if task.tags else "",
                    })

            return True

        except Exception as e:
            print(f"CSV export failed: {e}")
            return False