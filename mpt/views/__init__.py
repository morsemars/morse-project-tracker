from flask import jsonify
from mpt.views.login import setup_login
from mpt.views.projects import setup_projects
from mpt.views.tasks import setup_tasks
from mpt.views.users import setup_users
from mpt.views.activities import setup_activities


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
    setup_activities(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            "code": 404,
            "message": "Page Not Found"
        }), 404


    @app.errorhandler(422)
    def page_not_found(error):
        return jsonify({
            "success": False,
            "code": 422,
            "message": "Request Cannot Be Processed"
        }), 422

    @app.errorhandler(405)
    def page_not_found(error):
        return jsonify({
            "success": False,
            "code": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(500)
    def page_not_found(error):
        return jsonify({
            "success": False,
            "code": 500,
            "message": "Internal Server Error"
        }), 500

    