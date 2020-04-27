from flask import jsonify, redirect, request
from mpt.auth import login_url


def setup_login(app):
    @app.route('/login')
    def redirect_to_auth0():
        return redirect(login_url)
