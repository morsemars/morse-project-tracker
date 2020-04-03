from mpt.models import db
from mpt.models.base_model import base_model
from mpt.models.project import project_assignment
from sqlalchemy import Column, String, Integer, Text

class User(base_model):
    __tablename__ = "users"

    first_name = Column(String(50), nullable = False)
    last_name = Column(String(50), nullable = False)
    position = Column(String(15), nullable = False)
    tasks = db.relationship("Task", cascade="all, delete-orphan")
    projects = db.relationship("Project", secondary=project_assignment)

    def __repr__(self):
        return f'<User {self.first_name}, {self.tasks}, {self.projects}>'