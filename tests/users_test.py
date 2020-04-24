import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from mpt import create_app
from mpt.models import db
from mpt.models.user import User
from mpt.models.project import Project
from mpt.models.task import Task

from tests.config import TOKEN

class UsersTestCase(unittest.TestCase):
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
        
        if user is None:
            User(
                first_name = "Marcelino",
                last_name = "Madriaga",
                position = "Manager"
            ).insert()

            user = User.query.first()

        self.user_id = user.id

        if not user.projects:
            projects = Project.query.all()
            for project in projects:
                user.projects.append(project)
            user.update()

        self.new_task = {
            "name": "Test Task",
            "description": "This is the description for the task.",
            "status": "created",
            "project": user.projects[0].id
        }

        if not user.tasks:
            
            tasks = Task.query.all()

            if not tasks:
                Task(
                    name = self.new_task["name"],
                    description = self.new_task["description"],
                    status = self.new_task["status"],
                    project = self.new_task["project"]
                ).insert()
                tasks = Task.query.all()

            for task in tasks:
                user.tasks.append(task)
            user.update()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_add_new_user(self):
        res = self.client().post('/users', json = self.new_user, headers={'Authorization': TOKEN})
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_error_422_when_missing_user_properties(self):
        res = self.client().post('/users', json = {}, headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")
    
    def test_405_if_add_user_not_allowed(self):

        res = self.client().post('/users/20', json = self.new_user, headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_get_users(self):

        res = self.client().get('/users', headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['users'])

    def test_get_user_by_id(self):

        res = self.client().get('/users/{}'.format(self.user_id), headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['user'])

    def test_404_if_user_not_found(self):

        res = self.client().get('/users/99999', headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    
    def test_update_user_details(self):
        res = self.client().patch('/users/{}'.format(self.user_id), json={
            "first_name": "Marcelinoooo",
            "last_name":"Madriaga",
            "position": "Manager"
        }, headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['user'])

    def test_405_if_update_user_not_allowed(self):

        res = self.client().patch('/users', json = self.new_user, headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    
    def test_delete_user(self):

        res = self.client().delete('/users/{}'.format(self.user_id), headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_delete_user_not_exists(self):
        res = self.client().delete('/users/0', headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_405_if_delete_user_not_allowed(self):
        res = self.client().delete('/users', headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_get_user_projects(self):
        res = self.client().get('/users/{}/projects'.format(self.user_id), headers={'Authorization': TOKEN})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['projects'])

    def test_get_user_tasks(self):
        res = self.client().get('/users/{}/tasks'.format(self.user_id), headers={'Authorization': TOKEN})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['tasks'])

if __name__ == "__main__":
    unittest.main()