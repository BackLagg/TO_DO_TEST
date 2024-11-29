from Tasker.task_manager import TaskManager
from Tasker.validator import Validator


class Interface:
    def __init__(self, manager: TaskManager):
        self.manager = manager

    def view_tasks(self):
        self.manager.display_tasks()

    def add_task(self):
        title = input("Название: ").strip()
        description = input("Описание: ").strip()
        category = input("Категория: ").strip()
        days = Validator.input_days()
        priority = Validator.input_priority()
        self.manager.add_task(title, description, category, days, priority)

    def edit_task(self):
        task_id = Validator.input_task_id()  # Используем валидацию ID
        # Поиск задачи по ID
        task = self.manager.find_task_by_id(task_id)
        if not task:
            print(f"Задача с ID {task_id} не найдена. Редактирование невозможно.")
            return  # Прерываем выполнение функции, если задачи нет
        title = input("Новое название (оставьте пустым для пропуска): ").strip()
        description = input("Новое описание (оставьте пустым для пропуска): ").strip()
        category = input("Новая категория (оставьте пустым для пропуска): ").strip()
        days = Validator.input_days() if input("Изменить срок выполнения? (да/нет): ").strip().lower() == "да" else None
        priority = Validator.input_priority()
        update_data = {field_name: field_value for field_name, field_value in {
            "title": title,
            "description": description,
            "category": category,
            "priority": priority,
            "days": days
        }.items() if field_value}
        self.manager.edit_task(task_id, **update_data)

    def mark_task_done(self):
        task_id = int(input("ID задачи для отметки как выполненной: "))
        self.manager.mark_task_done(task_id)

    def delete_task(self):
        task_id = int(input("ID задачи для удаления: "))
        self.manager.delete_task(task_id)

    def search_tasks(self):
        keyword = input("Ключевое слово: ")
        category = input("Категория: ")
        status = input("Статус (выполнена/не выполнена): ")
        results = self.manager.search_tasks(keyword, category, status)
        self.manager.display_tasks(results)

    def exit_program(self):
        print("Выход...")
        return True  # Завершаем цикл

    def run(self):
        options = {
            "1": self.view_tasks,
            "2": self.add_task,
            "3": self.edit_task,
            "4": self.mark_task_done,
            "5": self.delete_task,
            "6": self.search_tasks,
            "7": self.exit_program
        }

        while True:
            print(
                "\n1. Просмотр задач\n2. Добавить задачу\n3. Изменить задачу\n4. Отметить как выполненную\n5. Удалить задачу\n6. Поиск задач\n7. Выйти")
            choice = input("Выберите действие: ")

            action = options.get(choice)
            if action:
                should_continue = action()
                if should_continue:
                    break
            else:
                print("Неверный выбор.")
