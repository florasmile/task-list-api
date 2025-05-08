from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]

    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

     #create an instance from a dictionary
    @classmethod
    def from_dict(cls, goal_data):
        return cls(
                title=goal_data["title"]
        )
    
    # Return a Python dictionary from a model instance
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }
    
    def to_nested_dict(self):
        return {
            "goal": self.to_dict()
        }
