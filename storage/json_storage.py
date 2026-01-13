import json
from storage.base import Storage
from models.task import Task

class JSONStorage(Storage):


        def save(self, tasks):
            """

            Конвертирует список объектов task.to_dict()).Storag.
            Task в список словарей (используя Записывает данные в JSON файл с отступами (indent=2)
            и поддержкой кириллицы (ensure_ascii=False).
            Возвращает True при успехе, False при ошибке

            """

            try:
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump(
                        [task.to_dict() for task in tasks],
                        f,
                        indent=2,
                        ensure_ascii=False
                    )
                return True
            except Exception:
                return False

        def load(self):
            """

            Если файл не существует — возвращает пустой список.
            Читает файл, парсит JSON и преобразует словари обратно в объекты
            (используяTask.from_dict()).
            Обрабатывает ошибку Taskjson.JSONDecodeError (если файл поврежден)

            """

            if not self.file_path.exists():
                return []

            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return [Task.from_dict(item) for item in data]
            except json.JSONDecodeError:
                return []

        def export(self, tasks, export_path):
            """

            Аналогичен методу save, но сохраняет данные по указанному пути export_path.
            Также должен проверять наличие директории перед записью

            """

            try:
                export_path.parent.mkdir(parents=True, exist_ok=True)
                with open(export_path, "w", encoding="utf-8") as f:
                    json.dump(
                        [task.to_dict() for task in tasks],
                        f,
                        indent=2,
                        ensure_ascii=False
                    )
                return True
            except Exception:
                return False
