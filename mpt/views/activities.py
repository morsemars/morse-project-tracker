from flask import request, jsonify, abort
from mpt.models.activity import Activity
from mpt.auth import requires_auth
from mpt.views.base import insert, get_all, get_one, update, delete


def setup_activities(app):

    @app.route('/activities')
    @requires_auth('get:activities')
    def get_activities(jwt):

        activities = Activity.query
        return get_all(activities, 'activities')

    @app.route('/activities', methods=['POST'])
    @requires_auth('post:activity')
    def add_activity(jwt):

        data = request.get_json()

        new_activity = Activity(
            description=data.get("description"),
            hours=data.get("hours"),
            task_id=data.get("task_id")
        )

        return insert(new_activity)

    @app.route('/activities/<id>', methods=["GET"])
    @requires_auth('get:activities')
    def get_activity_by_id(jwt, id):

        activity = Activity.query.filter_by(id=id)
        return get_one(activity, "activity")

    @app.route('/activities/<id>', methods=["PATCH"])
    @requires_auth('patch:activity')
    def update_activities(jwt, id):

        data = request.get_json()
        activity = Activity.query.filter_by(id=id).one_or_none()

        if activity is None:
            abort(404)

        activity.description = data.get("description")
        activity.hours = data.get("hours")

        return update(activity, 'activity')

    @app.route("/activities/<id>", methods=["DELETE"])
    @requires_auth('delete:activity')
    def delete_activity(jwt, id):

        activity = Activity.query.filter_by(id=id).one_or_none()

        if activity is None:
            abort(404)

        return delete(activity)
