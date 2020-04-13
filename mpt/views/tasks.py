from flask import request, abort
from mpt.models.task import Task
from mpt.views.base import insert, get_all, get_one, update, delete

def setup_tasks(app):

    @app.route('/tasks')
    def get_tasks():

        task = Task.query
        return get_all(task, 'tasks')
    
    @app.route('/tasks', methods=['POST'])
    def add_task():

        data = request.get_json()

        new_task = Task(
            name = data.get("name"),
            description = data.get("description"),
            status = data.get("status"),
            project = data.get("project")
        )
        
        return insert(new_task)

    @app.route('/tasks/<id>', methods=["GET"])
    def get_task_by_id(id):

        task = Task.query.filter_by(id = id)
        return get_one(task, "task")
        
    @app.route('/tasks/<id>', methods=["PATCH"])
    def update_tasks(id):

        data = request.get_json()
        task = Task.query.filter_by(id = id).one_or_none()

        if task is None:
            abort(404)

        task.name = data.get("name"),
        task.description = data.get("description"),
        task.status = data.get("status"),
        task.project = data.get("project")

        return update(task, 'task')

    @app.route("/tasks/<id>", methods=["DELETE"])
    def delete_task(id):

        task = Task.query.filter_by(id = id).one_or_none()

        if task is None:
            abort(404)

        return delete(task)