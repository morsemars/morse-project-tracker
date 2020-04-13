import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from mpt import create_app
from mpt.models import db
from mpt.models.task import Task
from mpt.models.activity import Activity

class ActivitiesTestCase(unittest.TestCase):
    def setUp(self):
        database_name = "mpt_test"
        database_path = "postgresql://{}/{}".format('postgres@localhost:5433', database_name)
        
        self.app = create_app(database_path=database_path)
        self.client = self.app.test_client
        db.create_all()

        task = Task.query.first()

        self.new_activity = {
            "description": "Activity description here.",
            "hours": 1,
            "task_id": task.id
        }

        activity = Activity.query.first()

        if activity is None:
            Activity(
                description= self.new_activity["description"],
                hours= self.new_activity["hours"],
                task_id= self.new_activity["task_id"]
            ).insert()
            activity = Activity.query.first()

        self.activity_id = activity.id
        
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_add_new_activity(self):
        
        res = self.client().post('/activities', json = self.new_activity)
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_error_422_when_missing_activity_properties(self):
        res = self.client().post('/activities', json = {})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request Cannot Be Processed")
    
    def test_405_if_add_activity_not_allowed(self):

        res = self.client().post('/activities/20', json = self.new_activity)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_get_activities(self):

        res = self.client().get('/activities')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['activities'])

    def test_get_activity_by_id(self):

        res = self.client().get('/activities/{}'.format(self.activity_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['activity'])

    def test_404_if_activity_not_found(self):

        res = self.client().get('/activities/0')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_update_activity_details(self):
        res = self.client().patch('/activities/{}'.format(self.activity_id), json={
            "description":"UPDATED ACTIVITY DESCRIPTION",
            "hours": 2,
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['activity'])

    def test_405_if_update_activity_not_allowed(self):

        res = self.client().patch('/activities', json = self.new_activity)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_delete_project(self):

        res = self.client().delete('/activities/{}'.format(self.activity_id))

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_delete_activity_not_exists(self):
        res = self.client().delete('/activities/0')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    def test_405_if_delete_activity_not_allowed(self):
        res = self.client().delete('/activities')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

if __name__ == "__main__":
    unittest.main()