"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)
db = SQLAlchemy()
ma = Marshmallow(app)

def create_app():
    """Construct the core application."""
    app.config.from_object("config.Config")
    db.init_app(app)
    with app.app_context():
        from . import routes  # Import routes

        db.create_all()  # Create database tables for our data models

        return app
