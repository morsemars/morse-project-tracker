import unittest
import json
from mpt.models.task import Task
from mpt.models.user import User
from tests.test_env import app
from tests.config import DEV_TOKEN, TOKEN


class UserRoleTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client

        task = Task.query.first()
        user = User.query.order_by(User.id.desc()).first()

        self.new_user = {
                "first_name": "Test",
                "last_name": "User",
                "position": "Developer"
        }

        self.new_activity = {
            "description": "Activity description here.",
            "hours": 1,
            "task_id": task.id
        }

        self.user_id = user.id

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_dev_add_activities(self):

        res = self.client().post(
            '/activities',
            json=self.new_activity,
            headers={'Authorization': DEV_TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_401_manager_add_activities(self):

        res = self.client().post(
            '/activities',
            json=self.new_activity,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "User does not have authorization")

    def test_401_dev_add_new_user(self):

        res = self.client().post(
            '/users',
            json=self.new_user,
            headers={'Authorization': DEV_TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "User does not have authorization")

    def test_manager_add_new_user(self):

        res = self.client().post(
            '/users',
            json=self.new_user,
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_401_dev_delete_user(self):

        res = self.client().delete(
            '/users/{}'.format(self.user_id),
            headers={'Authorization': DEV_TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "User does not have authorization")

    def test_manager_delete_user(self):

        res = self.client().delete(
            '/users/{}'.format(self.user_id),
            headers={'Authorization': TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == "__main__":
    unittest.main()
