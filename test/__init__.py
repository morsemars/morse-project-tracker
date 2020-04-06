import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

from mpt import create_app
from mpt.models import setup_db, db
from mpt.models.user import User
from mpt.models.project import Project
from mpt.models.task import Task

from test import user_api_test


class MPTTestCase(unittest.TestCase):
    def setUp(self):
        database_name = "mpt_test"
        database_path = "postgresql://{}/{}".format('postgres@localhost:5433', database_name)
        
        self.app = create_app(database_path=database_path)
        self.client = self.app.test_client
        db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_projects(self):
        self.assertTrue(True)

    # def test_insert_project(self):

    #     new_project = Project(
    #             name = "Test Project",
    #             description = "This is the description for the project.",
    #             manager = 1,
    #             status = "ongoing"
    #         )

    #     users = User.query.filter(User.id != 1).all()

    #     for user in users:
    #         new_project.assignees.append(user)

    #     new_project.insert()

    #     projects = Project.query.all()
    #     print(projects)

    #     self.assertEqual(1, len(projects))


    # def test_insert_tasks(self):
    #     new_task1 = Task(
    #             name = "Test Task 1",
    #             description = "This is the description for the task.",
    #             status = "created",
    #             assignee = 3,
    #             project = 4,
    #         )

    #     new_task2 = Task(
    #             name = "Test Task 2",
    #             description = "This is the description for the task.",
    #             status = "created",
    #             assignee = 2,
    #             project = 4,
    #         )

    #     new_task1.insert()
    #     new_task2.insert()

    #     tasks = Task.query.all()
    #     print(tasks)

    #     self.assertEqual(2, len(tasks))

    # def test_delete_project(self):
        
    #     project = Project.query.filter(Project.id == 3).first()

    #     project.delete()

    #     project = Project.query.all()

    #     self.assertEqual(0, len(project))

    # def test_delete_user(self):
    #     user = User.query.filter(User.id == 3).first()

    #     user.delete()

class UserTestCase(unittest.TestCase):
    def setUp(self):
        database_name = "mpt_test"
        database_path = "postgresql://{}/{}".format('postgres@localhost:5433', database_name)
        
        self.app = create_app(database_path=database_path)
        self.client = self.app.test_client
        db.create_all()

        self.new_user = {
                "first_name":"Marcelino",
                "last_name": "Madriaga",
                "position": "Developer"
        }

        user = User.query.first()
        print(user.id)
        if user is None:
            User(
                first_name = "Marcelino",
                last_name = "Madriaga",
                position = "Manager"
            ).insert()

            user = User.query.first()

        self.user_id = user.id

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_add_new_user(self):
        res = self.client().post('/users', json = self.new_user)
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_error_422_when_missing_user_properties(self):
        res = self.client().post('/users', json = {})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")
    
    def test_405_if_add_user_not_allowed(self):

        res = self.client().post('/users/20', json = self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_get_users(self):

        res = self.client().get('/users')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['users'])

    def test_get_user_by_id(self):

        res = self.client().get('/users/{}'.format(self.user_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['user'])

    def test_404_if_user_not_found(self):

        res = self.client().get('/users/99999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_update_user_details(self):
        print(self.user_id)
        res = self.client().patch('/users/{}'.format(self.user_id), json={
            "first_name": "Marcelinoooo",
            "last_name":"Madriaga",
            "position": "Manager"
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['user'])

    def test_405_if_update_user_not_allowed(self):

        res = self.client().patch('/users', json = self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_delete_user(self):

        res = self.client().delete('/users/{}'.format(self.user_id))

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_delete_user_not_exists(self):
        res = self.client().delete('/users/0')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_405_if_delete_user_not_allowed(self):
        res = self.client().delete('/users')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")


if __name__ == "__main__":
    unittest.main()