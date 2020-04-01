from flask import jsonify

def setup_login(app):
    @app.route('/login')
    def test_login():
        return jsonify({
            'success': True,
            'route': 'Login'
        })