from mpt.models.base_model import base_model
from sqlalchemy import Column, String, Integer, Text, Date, Time, ForeignKey

class Task(base_model):
    __tablename__ = "task"

    name = Column(String(50), nullable = False)
    description = Column(Text, nullable = False)
    status = Column(String, nullable = False)
    comments = Column(Text, nullable = True)
    estimated_delivery = Column(Date, nullable = True)
    actual_delivery = Column(Date, nullable = True)
    time_spent = Column(Time, nullable = True)
    project = Column(Integer, ForeignKey('project.id'))
    assignee = Column(Integer, ForeignKey('user.id'))