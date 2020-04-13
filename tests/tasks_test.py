import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from mpt import create_app
from mpt.models import db
from mpt.models.user import User
from mpt.models.task import Task
from mpt.models.project import Project

class TasksTestCase(unittest.TestCase):
    def setUp(self):
        database_name = "mpt_test"
        database_path = "postgresql://{}/{}".format('postgres@localhost:5433', database_name)
        
        self.app = create_app(database_path=database_path)
        self.client = self.app.test_client
        db.create_all()

        task = Task.query.first()
        project = Project.query.first()
        dev = User.query.first()

        self.new_task = {
            "name": "Test Task",
            "description": "This is the description for the task.",
            "status": "created",
            "project": project.id
        }

        if task is None:
            Task(
                name = self.new_task["name"],
                description = self.new_task["description"],
                status = self.new_task["status"],
                project = self.new_task["project"]
            ).insert()
            task = Task.query.first()

        self.task_id = task.id
        self.dev_id = dev.id

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_add_task(self):

        res = self.client().post('/tasks', json = self.new_task)
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

  

    def test_error_422_when_missing_task_properties(self):
        res = self.client().post('/tasks', json = {})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_get_tasks(self):

        res = self.client().get('/tasks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['tasks'])

    def test_get_task_by_id(self):

        res = self.client().get('/tasks/{}'.format(self.task_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['task'])

    def test_404_if_task_not_found(self):

        res = self.client().get('/tasks/0')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_405_if_add_task_not_allowed(self):

        res = self.client().post('/tasks/20', json = self.new_task)
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
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['task'])

    def test_405_if_update_task_not_allowed(self):

        res = self.client().patch('/tasks', json = self.new_task)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    
    def test_delete_task(self):

        res = self.client().delete('/tasks/{}'.format(self.task_id))

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_delete_task_not_exists(self):
        res = self.client().delete('/tasks/0')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_405_if_delete_task_not_allowed(self):
        res = self.client().delete('/tasks')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    # def test_get_user_projects(self):
    #     res = self.client().get('/tasks/{}/projects'.format(self.user_id))

    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['projects'])

if __name__ == "__main__":
    unittest.main()