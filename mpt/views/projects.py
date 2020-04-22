from flask import jsonify, request, abort
from mpt.models.project import Project
from mpt.models.user import User
from mpt.auth import requires_auth
from mpt.views.base import insert, get_all, get_one, update, delete

def setup_projects(app):

    @app.route('/projects')
    #@requires_auth('get:projects')
    #def get__projects(jwt):
    def get_projects():

        projects = Project.query
        return get_all(projects, 'projects')

    @app.route('/projects', methods=["POST"])
    def add_new_project():
        data = request.get_json()

        manager_id = data.get("manager")

        user = User.query.filter_by(id = manager_id).one_or_none()

        if user is None:
            abort(422)

        if user.position != "Manager":
            abort(422)

        print(data.get("manager"))

        new_project = Project(
            name = data.get("name"),
            description = data.get("description"),
            manager = data.get("manager"),
            status = data.get("status")
        )

        return insert(new_project) 

    @app.route('/projects/<id>', methods=["GET"])
    def get_project_by_id(id):

        project = Project.query.filter_by(id = id)
        return get_one(project, "project")
    
    @app.route('/projects/<id>', methods=["PATCH"])
    def update_project(id):
        #TODO: add assignee validation

        data = request.get_json()
        assignees = data.get("assignees")

        project = Project.query.filter_by(id = id).one_or_none()
    
        if project is None:
            abort(404)

        new_assigness = User.query.filter(User.id.in_(assignees)).all()

        project.name = data.get("name")
        project.description = data.get("description")
        project.manager = data.get("manager")
        project.status = data.get("status")
        project.assignees = new_assigness

        return update(project, "project")

    @app.route("/projects/<id>", methods=["DELETE"])
    def delete_project(id):

        project = Project.query.filter_by(id = id).one_or_none()

        if project is None:
            abort(404)

        return delete(project)

    @app.route('/projects/<id>/tasks', methods=["GET"])
    def get_project_tasks(id):

        project = Project.query.filter_by(id = id).one_or_none()
 
        if project is None:
            abort(404)

        tasks = [task._asdict() for task in project.tasks]

        return jsonify({
            'success': True,
            'tasks': tasks
        })