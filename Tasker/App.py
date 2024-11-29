from task_manager import TaskManager
from interface import Interface


if __name__ == "__main__":
    manager = TaskManager()
    interface = Interface(manager)
    interface.run()
