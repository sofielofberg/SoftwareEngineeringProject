# Setup inspired by
# https://flask.palletsprojects.com/en/stable/patterns/packages/

from flask import Flask
from flask_login import LoginManager

import database
import user

# Start flask
app = Flask(__name__)
app.secret_key = "SECRET TUNNEL!!"

# Initialize database
database.init_db(app)
database.setup_db(app)

# Login
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return user.User.get_by_id(user_id)


# Import the views
import views  # noqa: F401
