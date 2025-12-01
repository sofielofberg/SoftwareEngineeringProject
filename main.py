# Setup inspired by
# https://flask.palletsprojects.com/en/stable/patterns/packages/

import os

from flask import Flask

import database
import login

# Start flask
app = Flask(__name__)
app.secret_key = "SECRET TUNNEL!!"
app.config["UPLOAD_FOLDER"] = "receipts"

# Initialize database
database.init_db(app, "sqlite:///database.db")
database.setup_db(app)

# Login
login.init_login_manager(app)

# Create folder for the receipt images (if it does not exist)
os.makedirs("receipts", exist_ok=True)

# Import the views
import views  # noqa: F401
