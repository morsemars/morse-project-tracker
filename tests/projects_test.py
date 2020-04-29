import unittest
import json
from mpt.models.user import User
from mpt.models.project import Project
from tests.config import TOKEN
from tests.test_env import app


class ProjectsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client

        manager = User.query.filter_by(position="Manager").first()
        dev = User.query.filter_by(position="Developer").first()

        self.new_project = {
            "name": "Test Project",
            "description": "This is the description for the project.",
            "manager": manager.id,
            "status": "ongoing"
        }

        project = Project.query.order_by(Project.id.desc()).first()

        self.project_id = project.id
        self.manager_id = manager.id
        self.dev_id = dev.id

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_add_new_project(self):

        res = self.client().post(
            '/projects',
            json=self.new_project,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_422_when_manager_id_is_not_found(self):

        self.new_project["manager"] = 0

        res = self.client().post(
            '/projects',
            json=self.new_project,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_422_when_user_not_manager(self):

        self.new_project["manager"] = self.dev_id

        res = self.client().post(
            '/projects',
            json=self.new_project,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_422_when_missing_project_properties(self):

        res = self.client().post(
            '/projects',
            json={},
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_405_if_add_project_not_allowed(self):

        res = self.client().post(
            '/projects/20',
            json=self.new_project,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_get_projects(self):

        res = self.client().get(
            '/projects',
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['projects'])

    def test_get_project_by_id(self):

        res = self.client().get(
            '/projects/{}'.format(self.project_id),
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])

    def test_404_if_project_not_found(self):

        res = self.client().get(
            '/projects/99999',
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_update_project_details(self):
        res = self.client().patch(
            '/projects/{}'.format(self.project_id),
            json={
                "name": "Test Project",
                "description": "UPDATED PROJECT DESCRIPTION",
                "manager": self.manager_id,
                "status": "ongoing",
                "assignees": [self.dev_id]
            },
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])

    def test_405_if_update_project_not_allowed(self):

        res = self.client().patch(
            '/projects',
            json=self.new_project,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_delete_project(self):

        res = self.client().delete(
            '/projects/{}'.format(self.project_id),
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_delete_project_not_exists(self):

        res = self.client().delete(
            '/projects/0',
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_405_if_delete_project_not_allowed(self):

        res = self.client().delete(
            '/projects',
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_get_project_tasks(self):
        res = self.client().get(
            '/projects/{}/tasks'.format(self.project_id),
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['tasks'])


if __name__ == "__main__":
    unittest.main()
