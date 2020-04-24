import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from mpt import create_app
from mpt.models import db
from mpt.models.user import User
from mpt.models.project import Project
from mpt.models.task import Task

from tests.config import TOKEN

class ProjectsTestCase(unittest.TestCase):
    def setUp(self):
        database_name = "mpt_test"
        database_path = "postgresql://{}/{}".format('postgres@localhost:5433', database_name)
        
        self.app = create_app(database_path=database_path)
        self.client = self.app.test_client
        db.create_all()

        manager = User.query.filter_by(position="Manager").one_or_none()

        dev = User.query.filter_by(position="Developer").one_or_none()

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

        project = Project.query.first()
        
        if project is None:
            Project(
                name = self.new_project["name"],
                description =self.new_project["description"],
                manager = self.new_project["manager"],
                status = self.new_project["status"]
            ).insert()

            project = Project.query.first()

        self.new_task = {
            "name": "Test Task",
            "description": "This is the description for the task.",
            "status": "created",
            "project": project.id
        }

        self.project_id = project.id
        self.manager_id = manager.id
        self.dev_id = dev.id

        if not project.tasks:
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
                project.tasks.append(task)
            project.update()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_add_new_project(self):

        res = self.client().post('/projects', json = self.new_project, headers={'Authorization': TOKEN})
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_422_when_manager_id_is_not_found(self):

        self.new_project["manager"] = 0

        res = self.client().post('/projects', json = self.new_project, headers={'Authorization': TOKEN})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_422_when_user_not_manager(self):

        self.new_project["manager"] = self.dev_id

        res = self.client().post('/projects', json = self.new_project, headers={'Authorization': TOKEN})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_422_when_missing_project_properties(self):
        res = self.client().post('/projects', json = {}, headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")
    
    def test_405_if_add_project_not_allowed(self):

        res = self.client().post('/projects/20', json = self.new_project, headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_get_projects(self):

        res = self.client().get('/projects', headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['projects'])

    def test_get_project_by_id(self):

        res = self.client().get('/projects/{}'.format(self.project_id), headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])

    def test_404_if_project_not_found(self):

        res = self.client().get('/projects/99999', headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_update_project_details(self):
        res = self.client().patch('/projects/{}'.format(self.project_id), json={
            "name":"Test Project",
            "description":"UPDATED PROJECT DESCRIPTION",
            "manager": self.manager_id,
            "status":"ongoing",
            "assignees": [self.dev_id]
        }, headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])

    def test_405_if_update_project_not_allowed(self):

        res = self.client().patch('/projects', json = self.new_project, headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_delete_project(self):

        res = self.client().delete('/projects/{}'.format(self.project_id), headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_delete_project_not_exists(self):
        res = self.client().delete('/projects/0', headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_405_if_delete_project_not_allowed(self):
        res = self.client().delete('/projects', headers={'Authorization': TOKEN})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_get_project_tasks(self):
        res = self.client().get('/projects/{}/tasks'.format(self.project_id), headers={'Authorization': TOKEN})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['tasks'])

if __name__ == "__main__":
    unittest.main()