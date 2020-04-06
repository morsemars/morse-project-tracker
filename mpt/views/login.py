from flask import jsonify, redirect, request
#from mpt.auth import oauth, AUTH0_CALLBACK_URL, AUTH0_AUDIENCE
from mpt.auth import login_url

def setup_login(app):
    @app.route('/login')
    def redirect_to_auth0():
        return redirect(login_url)
        #return oauth.auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)
