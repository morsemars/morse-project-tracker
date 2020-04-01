from flask import jsonify
from mpt.models.user import User

def setup_users(app):
    @app.route('/users')
    def test_users():

        new_user = User(
            first_name = "Mars",
            last_name = "Mads",
            position = "Developer"
        )

        new_user.insert()

        return jsonify({
            'success': True,
            'route': 'Users',
            'user': new_user.format()
        })