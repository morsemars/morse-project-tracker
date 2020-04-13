from flask import request, jsonify, abort
from mpt.models.activity import Activity
from mpt.views.base import insert, get_all, get_one, update, delete

def setup_activities(app):
    @app.route('/activities')
    def get_activities():

        activities = Activity.query
        return get_all(activities, 'activities')
    
    @app.route('/activities', methods=['POST'])
    def add_activity():

        data = request.get_json()

        new_activity = Activity(
            description = data.get("description"),
            hours = data.get("hours"),
            task_id = data.get("task_id")
        )
        
        return insert(new_activity)

    @app.route('/activities/<id>', methods=["GET"])
    def get_activity_by_id(id):

        activity = Activity.query.filter_by(id = id)
        return get_one(activity, "activity")
        
    @app.route('/activities/<id>', methods=["PATCH"])
    def update_activities(id):

        data = request.get_json()
        activity = Activity.query.filter_by(id = id).one_or_none()

        if activity is None:
            abort(404)

        activity.description = data.get("description")
        activity.hours = data.get("hours")

        return update(activity, 'activity')

    @app.route("/activities/<id>", methods=["DELETE"])
    def delete_activity(id):

        activity = Activity.query.filter_by(id = id).one_or_none()

        if activity is None:
            abort(404)

        return delete(activity)
