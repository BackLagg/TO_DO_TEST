class Task:
    def __init__(self, id: int, title: str, description: str, category: str, due_date: str, priority: str,
                 status: str = "Не выполнена"):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        return Task(**data)
