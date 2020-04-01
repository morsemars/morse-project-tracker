from flask import jsonify
from .login import setup_login
from .projects import setup_projects
from .tasks import setup_tasks
from .users import setup_users

def setup_views(app):
    @app.route('/')
    def test():
        return jsonify({
            'success': True,
            'route': 'root'
        })

    setup_login(app)
    setup_projects(app)
    setup_tasks(app)
    setup_users(app)

    