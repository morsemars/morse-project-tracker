from flask import jsonify

def setup_projects(app):
    @app.route('/projects')
    def test_projects():
        return jsonify({
            'success': True,
            'route': 'Projects'
        })