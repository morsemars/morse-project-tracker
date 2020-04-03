from mpt.models.base_model import base_model
from sqlalchemy import Column, Integer, Text, ForeignKey

class Activity(base_model):
    __tablename__ = "activities"

    task_id = Column(Integer, ForeignKey('tasks.id'))
    description = Column(Text, nullable = False)
    hours = Column(Integer, nullable = False)

    def __repr__(self):
        return f'<Activity {self.id}, {self.hours}>'