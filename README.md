```
task_manager/
├── main.py                 # Точка входа
├── models/
│   ├── __init__.py
│   ├── task.py            # Модель Task
│   └── enums.py           # Priority, TaskStatus
├── strategies/
│   ├── __init__.py
│   ├── base.py            # Базовый класс Strategy
│   ├── deadline.py        # DeadlinePriorityStrategy
│   └── importance.py      # ImportancePriorityStrategy
├── observers/
│   ├── __init__.py
│   ├── base.py            # Базовый Observer
│   ├── logger.py          # LoggerObserver
│   └── notifier.py        # NotificationObserver
├── storage/
│   ├── __init__.py
│   ├── base.py            # Абстрактный Storage
│   ├── json_storage.py    # JSONStorage
│   └── csv_storage.py     # CSVStorage
├── services/
│   ├── __init__.py
│   └── task_manager.py    # TaskManager
├── utils/
│   ├── __init__.py
│   ├── logger.py          # Настройка логирования
│   └── validators.py      # Валидаторы
├── data/
│   ├── tasks.json         # Данные задач
│   ├── history.json       # История изменений
│   └── tasks.csv          # Экспорт в CSV
├── logs/
│   └── task_manager.log   # Логи
├── tests/
│   ├── __init__.py
│   ├── test_task.py
│   └── test_manager.py
└── requirements.txt
```