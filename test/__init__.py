import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from mpt import create_app
from mpt.models import setup_db, db
from mpt.models.user import User


class MPTTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "mpt_test"
        #database_path = "postgresql://postgres@localhost:5433/project_tracker"
        """Define test variables and initialize app."""

        self.database_path = "postgresql://{}/{}".format('postgres@localhost:5433', self.database_name)
        #setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_422_if_question_not_found(self):

        self.assertEqual(422, 422)


if __name__ == "__main__":
    MPTTestCase()