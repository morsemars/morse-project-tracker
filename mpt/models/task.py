from mpt.models import db
from mpt.models.base_model import base_model
from sqlalchemy import Column, String, Integer, Text, Date, Time, ForeignKey


class Task(base_model):
    __tablename__ = "tasks"

    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    estimated_delivery = Column(Date, nullable=True)
    actual_delivery = Column(Date, nullable=True)
    project = Column(Integer, ForeignKey('projects.id'))
    assignee = Column(Integer, ForeignKey('users.id'))
    activities = db.relationship("Activity", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Task {self.name}, {self.assignee}, {self.project}>'
