import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from mpt import create_app
from mpt.models import db
from mpt.models.user import User
from tests.test_env import app
from tests.config import TOKEN


class UsersTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client

        self.new_user = {
                "first_name": "Test",
                "last_name": "User",
                "position": "Developer"
        }

        user = User.query.order_by(User.id.desc()).first()
        self.user_id = user.id

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_add_new_user(self):

        res = self.client().post(
            '/users',
            json=self.new_user,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_error_422_when_missing_user_properties(self):

        res = self.client().post(
            '/users',
            json={},
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")

    def test_405_if_add_user_not_allowed(self):

        res = self.client().post(
            '/users/20',
            json=self.new_user,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_get_users(self):

        res = self.client().get(
            '/users',
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['users'])

    def test_get_user_by_id(self):

        res = self.client().get(
            '/users/{}'.format(self.user_id),
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['user'])

    def test_404_if_user_not_found(self):

        res = self.client().get(
            '/users/99999',
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_update_user_details(self):

        res = self.client().patch(
            '/users/{}'.format(self.user_id),
            json={
                "first_name": "UPDATED TEST",
                "last_name": "USER",
                "position": "Manager"
            },
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['user'])

    def test_405_if_update_user_not_allowed(self):

        res = self.client().patch(
            '/users',
            json=self.new_user,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_delete_user(self):

        res = self.client().delete(
            '/users/{}'.format(self.user_id),
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_delete_user_not_exists(self):

        res = self.client().delete(
            '/users/0',
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_405_if_delete_user_not_allowed(self):

        res = self.client().delete(
            '/users',
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_get_user_projects(self):

        res = self.client().get(
            '/users/{}/projects'.format(self.user_id),
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['projects'])

    def test_get_user_tasks(self):

        res = self.client().get(
            '/users/{}/tasks'.format(self.user_id),
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['tasks'])


if __name__ == "__main__":
    unittest.main()
