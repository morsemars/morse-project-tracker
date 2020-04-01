from flask import jsonify

def setup_tasks(app):
    @app.route('/tasks')
    def test_tasks():
        return jsonify({
            'success': True,
            'route': 'Tasks'
        })