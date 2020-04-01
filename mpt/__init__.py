from flask import Flask
from flask_cors import CORS
from mpt.models import setup_db
from mpt.views import setup_views

def create_app(test_config=None):
    app = Flask(__name__)
    setup_views(app)
    setup_db(app)
    CORS(app)

    return app

app = create_app()
