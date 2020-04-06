from flask import Flask
from flask_cors import CORS
from mpt.models import setup_db
from mpt.views import setup_views

def create_app(test_config=None, database_path=None):
    app = Flask(__name__)
    app.secret_key = "SECRET HERE"#TODO: Transfer to separate file
    setup_views(app)
    setup_db(app, database_path)
    CORS(app)

    return app

app = create_app()
