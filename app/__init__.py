# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Create an instance of the Flask class.
myapp_obj = Flask(__name__)

# Create an instance of LoginManager, which will be used to manage Flask-Login.
login_manager = LoginManager()
# Configure LoginManager w/ Flask object
login_manager.init_app(myapp_obj)
login_manager.login_view = 'login'
login_manager.login_message = ('Please log in to access this page.')

# Get the base directory of the application to configure the database
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure Secret Key
# SQLALCHEMY_DATABASE_URI is the path to database.
myapp_obj.config.from_mapping(
    SECRET_KEY='you-will-never-guess',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Create SQLAlchemy object
db = SQLAlchemy(myapp_obj)

# Ensures that the database is accessible when handling a request
# After, database tables are created
with myapp_obj.app_context():
    from app.models import User

    db.create_all()

# Import the routes module from the 'app' package. This has the different urls for application
from app import routes

@login_manager.user_loader
def load_user(user_id):
    # Query the database to find a user by their ID.
    return User.query.get(int(user_id))