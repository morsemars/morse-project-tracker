from flask import request, abort, jsonify
from mpt.models.task import Task
from mpt.auth import requires_auth
from mpt.models.project import Project
from mpt.views.base import insert, get_all, get_one, update, delete

def setup_tasks(app):

    @app.route('/tasks')
    @requires_auth('get:tasks')
    def get_tasks(jwt):

        task = Task.query
        return get_all(task, 'tasks')
    
    @app.route('/tasks', methods=['POST'])
    @requires_auth('post:tasks')
    def add_task(jwt):

        data = request.get_json()
        project_id = data.get("project")
        project = Project.query.filter_by(id = project_id).one_or_none()

        if project is None:
            abort(422)

        new_task = Task(
            name = data.get("name"),
            description = data.get("description"),
            status = data.get("status"),
            project = project_id
        )
        
        return insert(new_task)

    @app.route('/tasks/<id>', methods=["GET"])
    @requires_auth('get:tasks')
    def get_task_by_id(jwt, id):

        task = Task.query.filter_by(id = id)
        return get_one(task, "task")
        
    @app.route('/tasks/<id>', methods=["PATCH"])
    @requires_auth('patch:task')
    def update_tasks(jwt,id):

        data = request.get_json()
        project_id = data.get("project")
        assignee_id = data.get("assignee")
        task = Task.query.filter_by(id = id).one_or_none()

        if task is None:
            abort(404)

        project = Project.query.filter_by(id = project_id).one_or_none()

        if project is None:
            abort(422)

        assignees = [assignee.id for assignee in project.assignees]

        if assignee_id not in assignees:
            abort(422)

        task.name = data.get("name"),
        task.description = data.get("description"),
        task.status = data.get("status"),
        task.project = project_id
        task.assignee = assignee_id

        return update(task, 'task')

    @app.route("/tasks/<id>", methods=["DELETE"])
    @requires_auth('delete:task')
    def delete_task(jwt,id):

        task = Task.query.filter_by(id = id).one_or_none()

        if task is None:
            abort(404)

        return delete(task)

    @app.route("/tasks/<id>/activities")
    @requires_auth('get:activities')
    def get_task_activities(jwt,id):

        task = Task.query.filter_by(id = id).one_or_none()

        if task is None:
            abort(404)

        activities = [activity._asdict() for activity in task.activities]

        return jsonify({
            'success': True,
            'activities': activities
        })