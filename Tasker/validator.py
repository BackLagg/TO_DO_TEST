class Validator:
    valid_priorities = {"низкий", "средний", "высокий"}

    @staticmethod
    def input_task_id() -> int:
        """Ввод ID задачи с проверкой на корректность."""
        while True:
            task_id = input("ID задачи для редактирования: ").strip()
            if task_id.isdigit():
                return int(task_id)
            print("Ошибка: Введите корректный числовой ID задачи.")

    @staticmethod
    def input_days() -> int:
        """Ввод количества дней с проверкой на корректность."""
        while True:
            days = input("Срок выполнения (в днях): ").strip()
            if not days:
                return 0  # Если оставили пустым, возвращаем 0
            if days.isdigit() and int(days) > 0:
                return int(days)
            print("Ошибка: Введите положительное целое число.")

    @staticmethod
    def input_priority() -> str:
        """Ввод приоритета с проверкой на допустимые значения."""
        while True:
            priority = input("Приоритет (низкий, средний, высокий): ").strip().lower()
            if priority in Validator.valid_priorities or not priority:
                return priority
            print("Ошибка: Введите один из вариантов: низкий, средний, высокий.")
