from mpt.models import db
from mpt.models.base_model import base_model
from mpt.models.project import project_assignment
from sqlalchemy import Column, String, Integer, Text

class User(base_model):
    __tablename__ = "user"

    first_name = Column(String(50), nullable = False)
    last_name = Column(String(50), nullable = False)
    position = Column(String(15), nullable = False)
    tasks = db.relationship("Task", backref="assignee")
    projects = db.relationship("Project", secondary=project_assignment, backref="assignees")