from flask import jsonify, request, abort
from mpt.models.user import User
from mpt.models import db
import traceback

def setup_users(app):

    @app.route('/users')
    def get_users():

        users = User.query.all()

        return jsonify({
            'success': True,
            'users': [user._asdict() for user in users]
        })

    @app.route('/users', methods=["POST"])
    def add_new_user():

        data = request.get_json()

        new_user = User(
            first_name = data.get("first_name"),
            last_name = data.get("last_name"),
            position = data.get("position")
        )

        isSuccessful = True

        try:
            new_user.insert()
        except:
            db.session.rollback()
            isSuccessful = False
        finally:
            if isSuccessful:
                return jsonify({
                    'success': True,
                    'created':  new_user.id,
                })
            else:
                abort(422)

    @app.route('/users/<id>', methods=["GET"])
    def get_user_by_id(id):

        user = User.query.filter_by(id = id).one_or_none()

        if user is None:
            abort(404)

        return jsonify({
            'success': True,
            'user': user._asdict()
        })

    @app.route('/users/<id>', methods=["PATCH"])
    def update_user(id):

        data = request.get_json()

        user = User.query.filter_by(id = id).one_or_none()

        if user is None:
            abort(404)

        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.position = data.get("position")

        isSuccessful = True

        try:
            user.update()
        except:
            db.session.rollback()
            isSuccessful = False
        finally:
            if isSuccessful:
                return jsonify({
                    'success': True,
                    'user': user._asdict()
                })
            else:
                abort(422)

    @app.route("/users/<id>", methods=["DELETE"])
    def delete_user(id):

        user = User.query.filter_by(id = id).one_or_none()

        if user is None:
            abort(404)

        isSuccessful = True

        try:
            user.delete()
        except:
            db.session.rollback()
            isSuccessful = False
        finally:
            if isSuccessful:
                return jsonify({
                    'success': True
                })
            else:
                abort(422)

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

        