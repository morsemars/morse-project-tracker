from flask import jsonify, request, abort
from mpt.models.project import Project
from mpt.auth import requires_auth
from mpt.models import db

def setup_projects(app):

    @app.route('/projects')
    #@requires_auth('get:projects')
    #def get__projects(jwt):
    def get_projects():

        projects = Project.query.all()

        if projects is None:
            abort(404)

        return jsonify({
            'success': True,
            'projects': [project._asdict() for project in projects]
        })

    @app.route('/projects', methods=["POST"])
    def add_new_project():
        data = request.get_json()

        new_project = Project(
            name = data.get("name"),
            description = data.get("description"),
            manager = data.get("manager"),
            status = data.get("status")
        )

        isSuccessful = True

        try:
            new_project.insert()
        except:
            
            db.session.rollback()
            isSuccessful = False
        finally:
            if isSuccessful:
                return jsonify({
                    'success': True,
                    'created':  new_project.id,
                })
            else:
                abort(422)

    @app.route('/projects/<id>', methods=["GET"])
    def get_project_by_id(id):

        project = Project.query.filter_by(id = id).one_or_none()

        if project is None:
            abort(404)

        return jsonify({
            'success': True,
            'project': project._asdict()
        })
    
    @app.route('/projects/<id>', methods=["PATCH"])
    def update_project(id):

        data = request.get_json()

        project = Project.query.filter_by(id = id).one_or_none()

        if project is None:
            abort(404)

        project.name = data.get("name"),
        project.description = data.get("description"),
        project.manager = data.get("manager"),
        project.status = data.get("status")

        isSuccessful = True

        try:
            project.update()
        except:
            db.session.rollback()
            isSuccessful = False
        finally:
            if isSuccessful:
                return jsonify({
                    'success': True,
                    'project': project._asdict()
                })
            else:
                abort(422)

    @app.route("/projects/<id>", methods=["DELETE"])
    def delete_project(id):

        project = Project.query.filter_by(id = id).one_or_none()

        if project is None:
            abort(404)

        isSuccessful = True

        try:
            project.delete()
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