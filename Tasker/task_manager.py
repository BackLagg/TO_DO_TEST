import json
from datetime import datetime, timedelta
from typing import List, Optional
from Tasker.models import Task
import os


class TaskManager:
    def __init__(self, filename: str = "data_base/tasks.json"):
        # Инициализация менеджера задач
        self.filename = filename
        self.tasks: List[Task] = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        # Создаем папку data_base, если ее нет
        if not os.path.exists("data_base"):
            os.makedirs("data_base")
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                return [Task.from_dict(task) for task in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self) -> None:
        """Сохранение задач в файл"""
        with open(self.filename, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4, ensure_ascii=False)

    def add_task(self, title: str, description: str, category: str, days: int, priority: str) -> None:
        """Добавление новой задачи."""
        task_id = max((task.id for task in self.tasks), default=0) + 1
        due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        new_task = Task(task_id, title, description, category, due_date, priority)
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"Задача '{title}' добавлена с дедлайном {due_date}.")

    def edit_task(self, task_id: int, **kwargs) -> None:
        """Изменение задач"""
        task = self.find_task_by_id(task_id)
        if task:
            for key, value in kwargs.items():
                if key == "days":
                    # Добавляем дни к текущему сроку выполнения
                    current_due_date = datetime.strptime(task.due_date, "%Y-%m-%d")
                    new_due_date = (current_due_date + timedelta(days=value)).strftime("%Y-%m-%d")
                    task.due_date = new_due_date
                elif hasattr(task, key):
                    setattr(task, key, value)
            self.save_tasks()
            print(f"Задача с ID {task_id} обновлена.")
        else:
            print(f"Задача с ID {task_id} не найдена.")

    def mark_task_done(self, task_id: int) -> None:
        """Отметка статуса выполнения"""
        self.edit_task(task_id, status="Выполнена")

    def delete_task(self, task_id: int) -> None:
        """Удаление задачи"""
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()
        print(f"Задача с ID {task_id} удалена.")

    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        """Поиск по ID"""
        return next((task for task in self.tasks if task.id == task_id), None)

    def search_tasks(self, keyword: str = "", category: str = "", status: str = "") -> List[Task]:
        """Поиск задач по параметрам"""
        results = [task for task in self.tasks if
                   (keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()) and
                   (not category or task.category.lower() == category.lower()) and
                   (not status or task.status.lower() == status.lower())]
        return results

    def display_tasks(self, tasks: Optional[List[Task]] = None) -> None:
        """Отображение всех задач."""
        tasks = tasks or self.tasks
        for task in tasks:
            print(
                f"[{task.id}] {task.title} - {task.status} (Категория: {task.category}, Приоритет: {task.priority}, Срок: {task.due_date})")
