from flask import request, abort, jsonify
from mpt.models.user import User
from mpt.auth import requires_auth
from mpt.views.base import insert, get_all, get_one, update, delete

def setup_users(app):

    @app.route('/users')
    @requires_auth('get:users')
    def get_users(jwt):

        users = User.query
        return get_all(users, 'users')

    @app.route('/users', methods=["POST"])
    @requires_auth('post:user')
    def add_new_user(jwt):

        data = request.get_json()

        new_user = User(
            first_name = data.get("first_name"),
            last_name = data.get("last_name"),
            position = data.get("position")
        )

        return insert(new_user)

    @app.route('/users/<id>', methods=["GET"])
    @requires_auth('get:users')
    def get_user_by_id(jwt,id):

        user = User.query.filter_by(id = id)

        return get_one(user, "user")

    @app.route('/users/<id>', methods=["PATCH"])
    @requires_auth('patch:user')
    def update_user(jwt,id):

        data = request.get_json()

        user = User.query.filter_by(id = id).one_or_none()

        if user is None:
            abort(404)

        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.position = data.get("position")

        return update(user, "user")

    @app.route("/users/<id>", methods=["DELETE"])
    @requires_auth('delete:user')
    def delete_user(jwt, id):

        user = User.query.filter_by(id = id).one_or_none()

        if user is None:
            abort(404)

        return delete(user)

    @app.route('/users/<id>/projects', methods=["GET"])
    @requires_auth('get:projects')
    def get_user_projects(jwt, id):

        user = User.query.filter_by(id = id).one_or_none()

        if user is None:
            abort(404)

        projects = [project._asdict() for project in user.projects]

        return jsonify({
            'success': True,
            'projects': projects
        })

    @app.route('/users/<id>/tasks', methods=["GET"])
    @requires_auth('get:tasks')
    def get_user_tasks(jwt,id):

        user = User.query.filter_by(id = id).one_or_none()

        if user is None:
            abort(404)

        tasks = [task._asdict() for task in user.tasks]

        return jsonify({
            'success': True,
            'tasks': tasks
        })

        