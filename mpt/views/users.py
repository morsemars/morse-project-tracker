from flask import request, abort, jsonify
from mpt.models.user import User
from mpt.views.base import insert, get_all, get_one, update, delete

def setup_users(app):

    @app.route('/users')
    def get_users():

        users = User.query
        return get_all(users, 'users')

    @app.route('/users', methods=["POST"])
    def add_new_user():

        data = request.get_json()

        new_user = User(
            first_name = data.get("first_name"),
            last_name = data.get("last_name"),
            position = data.get("position")
        )

        return insert(new_user)

    @app.route('/users/<id>', methods=["GET"])
    def get_user_by_id(id):

        user = User.query.filter_by(id = id)

        return get_one(user, "user")

    @app.route('/users/<id>', methods=["PATCH"])
    def update_user(id):

        data = request.get_json()

        user = User.query.filter_by(id = id).one_or_none()

        if user is None:
            abort(404)

        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.position = data.get("position")

        return update(user, "user")

    @app.route("/users/<id>", methods=["DELETE"])
    def delete_user(id):

        user = User.query.filter_by(id = id).one_or_none()

        if user is None:
            abort(404)

        return delete(user)

    @app.route('/users/<id>/projects', methods=["GET"])
    def get_user_projects(id):

        user = User.query.filter_by(id = id).one_or_none()

        if user is None:
            abort(404)

        projects = [project._asdict() for project in user.projects]

        return jsonify({
            'success': True,
            'projects': projects
        })

        