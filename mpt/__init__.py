from flask import Flask
from flask_cors import CORS
from mpt.models import setup_db
from mpt.views import setup_views
import os


DEFAULT_DB_PATH = "postgresql://postgres@localhost:5433/project_tracker"

if "DATABASE_URL" in os.environ:
    DEFAULT_DB_PATH = os.environ["DATABASE_URL"]


def create_app(test_config=None, database_path=DEFAULT_DB_PATH):
    app = Flask(__name__)
    app.secret_key = "SECRET HERE"  # TODO: Transfer to separate file
    setup_views(app)
    setup_db(app, database_path)
    CORS(app)

    return app


app = create_app()
