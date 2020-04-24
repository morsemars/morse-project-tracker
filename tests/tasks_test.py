import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from mpt import create_app
from mpt.models import db
from mpt.models.user import User
from mpt.models.task import Task
from mpt.models.project import Project
from mpt.models.activity import Activity

from tests.config import TOKEN

class TasksTestCase(unittest.TestCase):
    def setUp(self):
        database_name = "mpt_test"
        database_path = "postgresql://{}/{}".format('postgres@localhost:5433', database_name)
        
        self.app = create_app(database_path=database_path)
        self.client = self.app.test_client
        db.create_all()

        project = Project.query.first()
        dev = User.query.filter_by(position="Developer").one_or_none()
        manager = User.query.filter_by(position="Manager").one_or_none()

        if manager is None:
            User(
                first_name = "Marcelino",
                last_name = "Madriaga",
                position = "Manager"
            ).insert()
            manager = User.query.filter_by(position="Manager").one_or_none()

        if dev is None:
            User(
                first_name = "Marcelino",
                last_name = "Madriaga",
                position = "Developer"
            ).insert()
            dev = User.query.filter_by(position="Developer").one_or_none()

        self.new_project = {
            "name":"Test Project",
            "description":"This is the description for the project.",
            "manager": manager.id,
            "status":"ongoing"
        }

        if project is None:
            Project(
                name = self.new_project["name"],
                description =self.new_project["description"],
                manager = self.new_project["manager"],
                status = self.new_project["status"],
                assignees = [dev]
            ).insert()
            project = Project.query.first()
        
        self.new_task = {
            "name": "Test Task",
            "description": "This is the description for the task.",
            "status": "created",
            "project": project.id
        }

        if not project.tasks:
            Task(
                name = self.new_task["name"],
                description = self.new_task["description"],
                status = self.new_task["status"],
                project = self.new_task["project"]
            ).insert()
            task = Task.query.first()
        else:
            task = project.tasks[0]

        self.new_activity = {
            "description": "Activity description here.",
            "hours": 1,
            "task_id": task.id
        }

        if not task.activities:
            task.activities.append(Activity(
                description = self.new_activity["description"],
                hours = self.new_activity["hours"],
                task_id = self.new_activity["task_id"]
            ))

        self.task_id = task.id
        self.dev_id = dev.id

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_add_task(self):

        res = self.client().post('/tasks', json = self.new_task, headers={'Authorization': TOKEN})
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

  
    def test_error_422_when_project_not_found(self):
        self.new_task["project"] = 0
        res = self.client().post('/tasks', json = self.new_task, headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_error_422_when_missing_task_properties(self):
        res = self.client().post('/tasks', json = {}, headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_get_tasks(self):

        res = self.client().get('/tasks', headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['tasks'])

    def test_get_task_by_id(self):

        res = self.client().get('/tasks/{}'.format(self.task_id), headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['task'])

    def test_404_if_task_not_found(self):

        res = self.client().get('/tasks/0', headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_405_if_add_task_not_allowed(self):

        res = self.client().post('/tasks/20', json = self.new_task, headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    
    def test_update_task_details(self):
        res = self.client().patch('/tasks/{}'.format(self.task_id), json={
            "name": "Test Task UPDATED",
            "description": "This is the description for the task.",
            "status": "created",
            "assignee": self.dev_id,
            "project": self.new_task["project"]
        }, headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['task'])

    def test_error_422_when_user_not_assigned_in_project(self):
        res = self.client().patch('/tasks/{}'.format(self.task_id), json={
            "name": "Test Task UPDATED",
            "description": "This is the description for the task.",
            "status": "created",
            "assignee": 0,
            "project": self.new_task["project"]
        }, headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_405_if_update_task_not_allowed(self):

        res = self.client().patch('/tasks', json = self.new_task, headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    
    def test_delete_task(self):

        res = self.client().delete('/tasks/{}'.format(self.task_id), headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_delete_task_not_exists(self):
        res = self.client().delete('/tasks/0', headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_405_if_delete_task_not_allowed(self):
        res = self.client().delete('/tasks', headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_get_task_activities(self):
        res = self.client().get('/tasks/{}/activities'.format(self.task_id), headers={'Authorization': TOKEN})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['activities'])

if __name__ == "__main__":
    unittest.main()