import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from mpt import create_app
from mpt.models import db
from mpt.models.user import User
from mpt.models.project import Project

class UserTestCase(unittest.TestCase):
    def setUp(self):
        database_name = "mpt_test"
        database_path = "postgresql://{}/{}".format('postgres@localhost:5433', database_name)
        
        self.app = create_app(database_path=database_path)
        self.client = self.app.test_client
        db.create_all()

        manager = User.query.filter_by(position="Manager").one_or_none()

        if manager is None:
            User(
                first_name = "Marcelino",
                last_name = "Madriaga",
                position = "Manager"
            ).insert()
            manager = User.query.filter_by(position="Manager").one_or_none()

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

        self.project_id = project.id
        self.manager_id = manager.id


    def tearDown(self):
        """Executed after reach test"""
        pass

    @unittest.skip("TEST")
    def test_add_new_project(self):
        
        res = self.client().post('/projects', json = self.new_project)
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_error_422_when_missing_project_properties(self):
        res = self.client().post('/projects', json = {})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")
    
    def test_405_if_add_project_not_allowed(self):

        res = self.client().post('/projects/20', json = self.new_project)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_get_projects(self):

        res = self.client().get('/projects')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['projects'])

    def test_get_project_by_id(self):

        res = self.client().get('/projects/{}'.format(self.project_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])

    def test_404_if_project_not_found(self):

        res = self.client().get('/projects/99999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_update_project_details(self):
        res = self.client().patch('/projects/{}'.format(self.project_id), json={
            "name":"Test Project",
            "description":"UPDATED PROJECT DESCRIPTION",
            "manager": self.manager_id,
            "status":"ongoing"
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])

    def test_405_if_update_project_not_allowed(self):

        res = self.client().patch('/projects', json = self.new_project)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_delete_project(self):

        res = self.client().delete('/projects/{}'.format(self.project_id))

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_delete_project_not_exists(self):
        res = self.client().delete('/projects/0')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_405_if_delete_project_not_allowed(self):
        res = self.client().delete('/projects')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

if __name__ == "__main__":
    unittest.main()