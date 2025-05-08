from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from datetime import datetime
from sqlalchemy import DateTime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))

    goal: Mapped["Goal"] = relationship(back_populates="tasks")

 #create a task instance from a dictionary
    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(
                title=task_data["title"],
                description=task_data["description"]
        )
        if "completed_at" in task_data:
            new_task.completed_at = task_data["completed_at"] 

        return new_task
    
    # Return a Python dictionary from a model instance
    def to_dict(self):

        response_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }
        if self.goal_id:
            response_dict["goal_id"] = self.goal_id
            
        response_dict["is_complete"] = True if self.completed_at else False

        return response_dict
    
    def to_nested_dict(self):
        return {
            "task": self.to_dict()
        }


