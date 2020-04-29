import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from mpt import create_app
from mpt.models import db
from mpt.models.user import User
from mpt.models.task import Task
from mpt.models.project import Project
from tests.test_env import app
from tests.config import TOKEN


class TasksTestCase(unittest.TestCase):
    def setUp(self):

        self.client = app.test_client

        project = Project.query.first()
        dev = User.query.filter_by(position="Developer").first()
        manager = User.query.filter_by(position="Manager").first()

        self.new_task = {
            "name": "Test Task",
            "description": "This is the description for the task.",
            "status": "created",
            "project": project.id
        }

        task = Task.query.order_by(Task.id.desc()).first()

        self.task_id = task.id
        self.dev_id = dev.id

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_add_task(self):

        res = self.client().post(
            '/tasks', json=self.new_task,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_error_422_when_project_not_found(self):

        self.new_task["project"] = 0

        res = self.client().post(
            '/tasks',
            json=self.new_task,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_error_422_when_missing_task_properties(self):

        res = self.client().post(
            '/tasks',
            json={},
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_get_tasks(self):

        res = self.client().get(
            '/tasks',
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['tasks'])

    def test_get_task_by_id(self):

        res = self.client().get(
            '/tasks/{}'.format(self.task_id),
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['task'])

    def test_404_if_task_not_found(self):

        res = self.client().get(
            '/tasks/0',
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_405_if_add_task_not_allowed(self):

        res = self.client().post(
            '/tasks/20',
            json=self.new_task,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_update_task_details(self):

        res = self.client().patch(
            '/tasks/{}'.format(self.task_id),
            json={
                "name": "Test Task UPDATED",
                "description": "This is the description for the task.",
                "status": "created",
                "assignee": self.dev_id,
                "project": self.new_task["project"]
            },
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['task'])

    def test_error_422_when_user_not_assigned_in_project(self):

        res = self.client().patch(
            '/tasks/{}'.format(self.task_id),
            json={
                "name": "Test Task UPDATED",
                "description": "This is the description for the task.",
                "status": "created",
                "assignee": 0,
                "project": self.new_task["project"]
            },
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_405_if_update_task_not_allowed(self):

        res = self.client().patch(
            '/tasks',
            json=self.new_task,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_delete_task(self):

        res = self.client().delete(
            '/tasks/{}'.format(self.task_id),
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_delete_task_not_exists(self):

        res = self.client().delete(
            '/tasks/0',
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_405_if_delete_task_not_allowed(self):

        res = self.client().delete(
            '/tasks',
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_get_task_activities(self):

        res = self.client().get(
            '/tasks/{}/activities'.format(self.task_id),
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['activities'])


if __name__ == "__main__":
    unittest.main()
