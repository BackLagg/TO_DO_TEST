from Tasker.task_manager import TaskManager
from Tasker.interface import Interface


if __name__ == "__main__":
    manager = TaskManager()
    interface = Interface(manager)
    interface.run()
