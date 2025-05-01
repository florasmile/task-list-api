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
        new_task = cls(
            id=task_data["id"],
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data["completed_at"] 
        )

        return new_task
    
    # Return a Python dictionary from a model instance
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed_at": self.completed_at
        }

