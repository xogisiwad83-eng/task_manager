from pathlib import Path
from datetime import datetime, timedelta

from models.task import Task
from models.enums import Priority, TaskStatus
from services.task_manager import TaskManager
from storage.json_storage import JSONStorage
from observers.logger import LoggerObserver
from observers.notifier import NotificationObserver
from strategies.deadline import DeadlinePriorityStrategy
from strategies.importance import ImportancePriorityStrategy
from strategies.combined import CombinedPriorityStrategy


def print_task_list(tasks: list, title: str = "Tasks"):
    """Красивый вывод списка задач"""
    print(f"\n{'='*60}")
    print(f"{title} ({len(tasks)})")
    print('='*60)
    
    if not tasks:
        print("Нет задач")
        return
    
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
        if task.description:
            print(f"   📝 {task.description}")
        if task.tags:
            print(f"   🏷️  {', '.join(task.tags)}")
        print()


def print_statistics(stats: dict):
    """Вывод статистики"""
    print(f"\n{'='*60}")
    print("📊 Статистика задач")
    print('='*60)
    print(f"Всего задач: {stats['total']}")
    print(f"Завершено: {stats['completed']}")
    print(f"Не завершено: {stats['incomplete']}")
    print(f"Просрочено: {stats['overdue']}")
    print(f"Процент выполнения: {stats['completion_rate']}%")
    
    print(f"\nПо приоритетам:")
    print(f"  🔴 Высокий: {stats['by_priority']['high']}")
    print(f"  🟡 Средний: {stats['by_priority']['medium']}")
    print(f"  🟢 Низкий: {stats['by_priority']['low']}")
    
    print(f"\nПо статусам:")
    print(f"  ⭕ TODO: {stats['by_status']['todo']}")
    print(f"  🔄 В работе: {stats['by_status']['in_progress']}")
    print(f"  ✅ Готово: {stats['by_status']['done']}")
    print(f"  ❌ Отменено: {stats['by_status']['cancelled']}")


def demo_basic_operations():
    """Демонстрация базовых операций"""
    print("\n🚀 Демонстрация Task Manager\n")
    
    # Создаём менеджер
    storage = JSONStorage(Path("data/tasks.json"))
    manager = TaskManager(storage)
    
    # Добавляем наблюдателей
    logger = LoggerObserver(Path("logs/task_manager.log"))
    notifier = NotificationObserver()
    
    manager.add_observer(logger)
    manager.add_observer(notifier)
    
    print("✅ Task Manager создан")
    print(f"📁 Хранилище: {storage.file_path}")
    print(f"📝 Логи: {logger.log_file}")
    
    # Создаём задачи
    print("\n--- Создание задач ---")
    
    task1 = Task(
        title="Изучить паттерны проектирования",
        description="Прочитать главы про Strategy и Observer",
        priority=Priority.HIGH,
        deadline=datetime.now() + timedelta(days=7),
        tags=["учёба", "программирование"]
    )
    
    task2 = Task(
        title="Купить продукты",
        description="Молоко, хлеб, яйца",
        priority=Priority.MEDIUM,
        deadline=datetime.now() + timedelta(days=1),
        tags=["быт"]
    )
    
    task3 = Task(
        title="Подготовить презентацию",
        description="Презентация по Python для студентов",
        priority=Priority.HIGH,
        deadline=datetime.now() + timedelta(days=3),
        tags=["работа", "преподавание"]
    )
    
    task4 = Task(
        title="Сходить в спортзал",
        description="Кардио тренировка",
        priority=Priority.LOW,
        tags=["здоровье", "спорт"]
    )
    
    manager.add_task(task1)
    manager.add_task(task2)
    manager.add_task(task3)
    manager.add_task(task4)
    
    print(f"✅ Добавлено {len(manager.get_all_tasks())} задач")
    
    # Показываем все задачи
    print_task_list(manager.get_all_tasks(), "Все задачи")
    
    # Фильтрация
    print("\n--- Фильтрация ---")
    high_priority = manager.get_tasks_by_priority(Priority.HIGH)
    print_task_list(high_priority, "Задачи с высоким приоритетом")
    
    # Сортировка по дедлайну
    print("\n--- Сортировка по дедлайну ---")
    strategy = DeadlinePriorityStrategy()
    sorted_tasks = manager.sort_tasks(strategy=strategy)
    print_task_list(sorted_tasks, f"Задачи (стратегия: {strategy.get_name()})")
    
    # Отмечаем задачу выполненной
    print("\n--- Выполнение задачи ---")
    manager.complete_task(task2.id)
    print(f"✅ Задача '{task2.title}' выполнена")
    
    # Обновление задачи
    print("\n--- Обновление задачи ---")
    manager.update_task(
        task4.id,
        status=TaskStatus.IN_PROGRESS,
        description="Кардио тренировка - 30 минут бега"
    )
    print(f"✅ Задача '{task4.title}' обновлена")
    
    # Поиск
    print("\n--- Поиск ---")
    results = manager.search_tasks("презентация")
    print_task_list(results, "Результаты поиска: 'презентация'")
    
    # Статистика
    stats = manager.get_statistics()
    print_statistics(stats)
    
    # Экспорт
    print("\n--- Экспорт ---")
    csv_path = Path("data/tasks_export.csv")
    manager.export_tasks(csv_path, format='csv')
    print(f"✅ Задачи экспортированы в {csv_path}")
    
    # История
    print("\n--- История изменений ---")
    history = manager.get_history(limit=10)
    print(f"Последние {len(history)} действий:")
    for entry in history:
        print(f"  {entry['timestamp']}: {entry['action']} - {entry['task_title']}")
    
    return manager


def demo_strategies():
    """Демонстрация разных стратегий сортировки"""
    print("\n\n🎯 Демонстрация стратегий приоритизации\n")
    
    # Создаём менеджер с задачами
    storage = JSONStorage(Path("data/tasks.json"))
    manager = TaskManager(storage)
    
    strategies = [
        DeadlinePriorityStrategy(),
        ImportancePriorityStrategy(),
        CombinedPriorityStrategy()
    ]
    
    for strategy in strategies:
        sorted_tasks = manager.sort_tasks(strategy=strategy)
        print_task_list(sorted_tasks, f"Стратегия: {strategy.get_name()}")


def interactive_mode():
    """Интерактивный режим"""
    storage = JSONStorage(Path("data/tasks.json"))
    manager = TaskManager(storage)
    
    # Добавляем наблюдателей
    logger = LoggerObserver(Path("logs/task_manager.log"))
    manager.add_observer(logger)
    
    print("\n" + "="*60)
    print("📋 Task Manager - Интерактивный режим")
    print("="*60)
    
    while True:
        print("\n--- Меню ---")
        print("1. Показать все задачи")
        print("2. Добавить задачу")
        print("3. Отметить задачу выполненной")
        print("4. Удалить задачу")
        print("5. Поиск")
        print("6. Фильтры")
        print("7. Статистика")
        print("8. Экспорт")
        print("0. Выход")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == '1':
            tasks = manager.get_all_tasks()
            print_task_list(tasks, "Все задачи")
        
        elif choice == '2':
            print("\n--- Новая задача ---")
            title = input("Название: ")
            description = input("Описание: ")
            
            print("Приоритет: 1-Низкий, 2-Средний, 3-Высокий")
            priority_choice = input("Выберите (2): ").strip() or "2"
            priority_map = {"1": Priority.LOW, "2": Priority.MEDIUM, "3": Priority.HIGH}
            priority = priority_map.get(priority_choice, Priority.MEDIUM)
            
            days = input("Дедлайн через сколько дней (Enter - без дедлайна): ").strip()
            deadline = None
            if days and days.isdigit():
                deadline = datetime.now() + timedelta(days=int(days))
            
            tags = input("Теги (через запятую): ").strip()
            tag_list = [t.strip() for t in tags.split(',')] if tags else []
            
            task = Task(
                title=title,
                description=description,
                priority=priority,
                deadline=deadline,
                tags=tag_list
            )
            
            manager.add_task(task)
            print("✅ Задача добавлена!")
        
        elif choice == '3':
            tasks = manager.get_incomplete_tasks()
            print_task_list(tasks, "Незавершённые задачи")
            
            if tasks:
                task_num = input("\nНомер задачи для выполнения: ").strip()
                if task_num.isdigit():
                    idx = int(task_num) - 1
                    if 0 <= idx < len(tasks):
                        manager.complete_task(tasks[idx].id)
                        print("✅ Задача выполнена!")
        
        elif choice == '4':
            tasks = manager.get_all_tasks()
            print_task_list(tasks, "Все задачи")
            
            if tasks:
                task_num = input("\nНомер задачи для удаления: ").strip()
                if task_num.isdigit():
                    idx = int(task_num) - 1
                    if 0 <= idx < len(tasks):
                        manager.delete_task(tasks[idx].id)
                        print("✅ Задача удалена!")
        
        elif choice == '5':
            query = input("Поисковый запрос: ")
            results = manager.search_tasks(query)
            print_task_list(results, f"Результаты поиска: '{query}'")
        
        elif choice == '6':
            print("\n--- Фильтры ---")
            print("1. По приоритету")
            print("2. По статусу")
            print("3. По тегу")
            print("4. Просроченные")
            
            filter_choice = input("Выберите фильтр: ").strip()
            
            if filter_choice == '1':
                print("1-Низкий, 2-Средний, 3-Высокий")
                p = input("Приоритет: ").strip()
                priority_map = {"1": Priority.LOW, "2": Priority.MEDIUM, "3": Priority.HIGH}
                if p in priority_map:
                    tasks = manager.get_tasks_by_priority(priority_map[p])
                    print_task_list(tasks, f"Приоритет: {priority_map[p].value}")
            
            elif filter_choice == '4':
                tasks = manager.get_overdue_tasks()
                print_task_list(tasks, "Просроченные задачи")
        
        elif choice == '7':
            stats = manager.get_statistics()
            print_statistics(stats)
        
        elif choice == '8':
            filename = input("Имя файла (tasks_export): ").strip() or "tasks_export"
            format_choice = input("Формат (json/csv): ").strip() or "csv"
            
            export_path = Path(f"data/{filename}.{format_choice}")
            success = manager.export_tasks(export_path, format=format_choice)
            
            if success:
                print(f"✅ Экспортировано в {export_path}")
        
        elif choice == '0':
            print("\n👋 До свидания!")
            break


def main():
    """Главная функция"""
    print("="*60)
    print("📋 Task Manager - Система управления задачами")
    print("="*60)
    print("\nВыберите режим:")
    print("1. Демонстрация")
    print("2. Демонстрация стратегий")
    print("3. Интерактивный режим")
    print("0. Выход")
    
    choice = input("\nВаш выбор: ").strip()
    
    if choice == '1':
        demo_basic_operations()
    elif choice == '2':
        demo_strategies()
    elif choice == '3':
        interactive_mode()
    else:
        print("До свидания!")


if __name__ == "__main__":
    main()
