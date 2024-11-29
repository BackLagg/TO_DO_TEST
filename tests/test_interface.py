import pytest
from Tasker.task_manager import TaskManager
from Tasker.interface import Interface


@pytest.fixture
def mock_input(monkeypatch):
    """Фикстура для замены input."""
    inputs = iter([])

    def fake_input(prompt=""):
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)

    def set_input(*args):
        nonlocal inputs
        inputs = iter(args)

    return set_input


@pytest.fixture
def mock_print(monkeypatch):
    """Фикстура для замены print."""
    printed_data = []

    def fake_print(*args):
        printed_data.append(" ".join(map(str, args)))

    monkeypatch.setattr("builtins.print", fake_print)

    return printed_data


@pytest.fixture
def app_interface():
    """Создание экземпляра приложения."""
    manager = TaskManager("tests/data_base/test_interface.json")
    interface = Interface(manager)
    return interface


def test_add_and_view_task(app_interface, mock_input, mock_print):
    """Тест добавления и отображения задачи."""
    mock_input(
        "2",  # Выбор добавления задачи
        "Тестовая задача",  # Название
        "Описание задачи",  # Описание
        "Работа",  # Категория
        "5",  # Срок выполнения в днях
        "средний",  # Приоритет
        "7"  # Выход из программы
    )
    app_interface.run()
    assert "Задача 'Тестовая задача' добавлена с дедлайном" in "\n".join(mock_print)


def test_delete_task(app_interface, mock_input, mock_print):
    """Тест удаления задачи."""
    # Добавляем задачу, чтобы было что удалять
    app_interface.manager.add_task("Удаляемая задача", "Описание", "Личное", 3, "низкий")

    mock_input(
        "5",  # Удаление задачи
        "1",  # ID задачи
        "7"  # Выход
    )
    app_interface.run()
    assert "Задача с ID 1 удалена." in "\n".join(mock_print)


def test_mark_task_done(app_interface, mock_input, mock_print):
    """Тест отметки задачи как выполненной."""
    app_interface.manager.add_task("Завершаемая задача", "Описание", "Проект", 2, "высокий")

    mock_input(
        "4",  # Отметить как выполненную
        "2",  # ID задачи
        "7"  # Выход
    )

    app_interface.run()

    assert "Задача с ID 2 обновлена." in "\n".join(mock_print)
    assert app_interface.manager.tasks[0].status == "Выполнена"


def test_edit_task(app_interface, mock_input, mock_print):
    """Тест редактирования задачи с корректными данными."""
    app_interface.manager.add_task("Задача", "Описание", "Категория", 5, "средний")

    mock_input (
        "3",
        "2",  # ID задачи для редактирования
        "Новое название",  # Новое название
        "Новое описание",  # Новое описание
        "Новая категория",  # Новая категория
        "да",  # Изменить срок выполнения?
        "7",  # Новые дни
        "средний",  # Новый приоритет
        "7"  # Выход
    )

    app_interface.run()
    assert "Задача с ID 2 обновлена." in "\n".join(mock_print)


def test_search_tasks(app_interface, mock_input, mock_print):
    """Тест поиска задач с корректными данными."""
    # Добавляем несколько задач для поиска
    app_interface.manager.add_task("Задача 1", "Описание 1", "Проект", 5, "низкий")
    app_interface.manager.add_task("Задача 2", "Описание 2", "Проект", 3, "средний")

    mock_input (
        "6",
        "Задача",  # Ключевое слово
        "Проект",  # Категория
        "не выполнена",  # Статус
        "7"
    )

    app_interface.run()
    assert "Задача 1" in "\n".join(mock_print)
    assert "Задача 2" in "\n".join(mock_print)


def test_invalid_task_id(app_interface, mock_input, mock_print):
    """Тест ввода некорректного ID задачи для редактирования."""
    mock_input (
        "3"
        "abc",  # Некорректный ID
        "7"
    )

    app_interface.run()
    assert "Неверный выбор." in "\n".join(mock_print)


def test_invalid_priority(app_interface, mock_input, mock_print):
    """Тест ввода некорректного приоритета задачи."""
    mock_input (
        "2",
        "Задача",  # Название
        "Описание",  # Описание
        "Проект",  # Категория
        "5",  # Количество дней
        "обычный",  # Некорректный приоритет
        "низкий",
        "7"
    )

    app_interface.run()
    assert "Ошибка: Введите один из вариантов: низкий, средний, высокий." in "\n".join(mock_print)


def test_invalid_days(app_interface, mock_input, mock_print):
    """Тест ввода некорректного значения для количества дней."""
    mock_input(
        "2",
        "Задача",  # Название
        "Описание",  # Описание
        "Проект",  # Категория
        "abc",  # Некорректные дни
        "5",  # Количество дней
        "низкий",
        "7"
    )

    app_interface.run()
    assert "Ошибка: Введите положительное целое число." in "\n".join(mock_print)