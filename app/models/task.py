from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from sqlalchemy import DateTime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

 #create a task instance from a dictionary
    @classmethod
    def from_dict(cls, task_data):
        if "completed_at" in task_data:
            new_task = cls(
                title=task_data["title"],
                description=task_data["description"],
                completed_at=task_data["completed_at"] 
            )
        else:
            new_task = cls(
                title=task_data["title"],
                description=task_data["description"]
            )

        return new_task
    
    # Return a Python dictionary from a model instance
    def to_dict(self):
        if not self.completed_at:
            return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": False
            }
        else:
            return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "completed_at": self.completed_at
            }
    
    def to_nested_dict(self):
        return {
            "task": self.to_dict()
        }


