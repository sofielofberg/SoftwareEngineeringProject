# Setup inspired by
# https://flask.palletsprojects.com/en/stable/patterns/packages/

from flask import Flask

import database
import login

# Start flask
app = Flask(__name__)
app.secret_key = "SECRET TUNNEL!!"

# Initialize database
database.init_db(app, "sqlite:///database.db")
database.setup_db(app)

# Login
login.init_login_manager(app)

# Import the views
import views  # noqa: F401
