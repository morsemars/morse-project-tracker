from mpt.models import db
from sqlalchemy import Column, String, Integer, Text

class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable = False)
    last_name = Column(String, nullable = False)
    position = Column(String, nullable = False)

    def __init__(self, first_name, last_name, position):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'position': self.position,
        }