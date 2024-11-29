import pytest
from datetime import datetime, timedelta
from Tasker.task_manager import TaskManager
from Tasker.models import Task


# Фикстура для TaskManager
@pytest.fixture
def task_manager():
    return TaskManager()


# Тест для добавления задачи
def test_add_task(mocker, task_manager):
    # Мокируем метод save_tasks
    mock_save_tasks = mocker.patch.object(task_manager, 'save_tasks')

    task_manager.tasks = []  # очищаем задачи перед тестом

    # Добавляем задачу
    task_manager.add_task("Test Task", "Test Description", "Test Category", 5, "высокий")

    # Проверяем, что задача добавлена
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == "Test Task"
    assert task_manager.tasks[0].description == "Test Description"
    assert task_manager.tasks[0].category == "Test Category"
    assert task_manager.tasks[0].priority == "высокий"
    assert task_manager.tasks[0].due_date  # Проверка на наличие даты

    # Убедимся, что метод save_tasks был вызван
    mock_save_tasks.assert_called_once()


# Тест для редактирования задачи
def test_edit_task(mocker, task_manager):
    # Мокируем save_tasks
    mock_save_tasks = mocker.patch.object(task_manager, 'save_tasks')

    # Инициализация задачи
    old_due_date = "2024-12-31"
    task_manager.tasks = [Task(1, "Old Title", "Old Description", "Old Category", old_due_date, "Medium")]

    # Редактируем задачу, добавляем 4 дня к дедлайну
    task_manager.edit_task(1, title="New Title", description="New Description", category="New Category", priority="высокий", days=4)

    # Проверяем, что задача была изменена
    task = task_manager.tasks[0]
    assert task.title == "New Title"
    assert task.description == "New Description"
    assert task.category == "New Category"
    assert task.priority == "высокий"

    # Проверяем дату: добавляем 4 дня к старой дате
    expected_due_date = (datetime.strptime(old_due_date, "%Y-%m-%d") + timedelta(days=4)).strftime("%Y-%m-%d")
    assert task.due_date == expected_due_date  # Проверка на дату с учетом добавленных дней

    # Убедимся, что метод save_tasks был вызван
    mock_save_tasks.assert_called_once()


# Тест для поиска задачи
def test_search_tasks(task_manager):
    task_manager.tasks = [
        Task(1, "Test Task 1", "Description 1", "Category 1", "2024-12-31", "высокий"),
        Task(2, "Test Task 2", "Description 2", "Category 2", "2024-12-31", "средний")
    ]

    # Поиск по ключевому слову
    result = task_manager.search_tasks(keyword="Test Task")
    assert len(result) == 2  # Ожидаем 2 задачи, которые содержат 'Test Task' в названии

    # Поиск по категории
    result = task_manager.search_tasks(category="Category 1")
    assert len(result) == 1  # Ожидаем 1 задачу с категорией 'Category 1'


# Тест для удаления задачи
def test_delete_task(mocker, task_manager):
    # Мокируем save_tasks
    mock_save_tasks = mocker.patch.object(task_manager, 'save_tasks')

    task_manager.tasks = [Task(1, "Test Task", "Description", "Category", "2024-12-31", "High")]

    # Удаляем задачу
    task_manager.delete_task(1)

    # Проверяем, что задача удалена
    assert len(task_manager.tasks) == 0

    # Убедимся, что метод save_tasks был вызван
    mock_save_tasks.assert_called_once()


# Тест для поиска задачи по ID
def test_find_task_by_id(task_manager):
    task_manager.tasks = [
        Task(1, "Test Task 1", "Description 1", "Category 1", "2024-12-31", "High"),
        Task(2, "Test Task 2", "Description 2", "Category 2", "2024-12-31", "Medium")
    ]

    # Поиск существующей задачи
    task = task_manager.find_task_by_id(1)
    assert task is not None
    assert task.title == "Test Task 1"

    # Поиск несуществующей задачи
    task = task_manager.find_task_by_id(999)
    assert task is None

