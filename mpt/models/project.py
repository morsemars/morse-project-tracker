from mpt.models import db
from mpt.models.base_model import base_model
from sqlalchemy import Column, String, Integer, Text, Table, ForeignKey

project_assignment = Table('project_assignment', db.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Project(base_model):
    __tablename__ = "projects"

    name = Column(String(50), nullable = False)
    description = Column(Text, nullable = False)
    manager = Column(Integer, nullable = False)
    status = Column(String, nullable = False)
    tasks = db.relationship("Task", cascade="all, delete-orphan")
    assignees = db.relationship("User", secondary=project_assignment)

    def __repr__(self):
        return f'<Project {self.name}, {self.assignees}, {self.tasks}>'