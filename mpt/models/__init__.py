import os
from flask_sqlalchemy import SQLAlchemy

DEFAULT_DB_PATH = "postgresql://postgres@localhost:5433/project_tracker"

if "DATABASE_URL" in os.environ:
    database_path = os.environ["DATABASE_URL"]
    
db = SQLAlchemy()

def setup_db(app, database_path=DEFAULT_DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.create_all()