# Setup inspired by
# https://flask.palletsprojects.com/en/stable/patterns/packages/

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

# Start flask
app = Flask(__name__)
app.secret_key = "SECRET TUNNEL!!"

# Database stuff
class Base(DeclarativeBase, MappedAsDataclass):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app, model_class=Base)

# Setup the database
import accountant
import admin
import manager
import receipt
import salesman
import user

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(manager.Manager("admin", "admin"))
    db.session.commit()

# Login
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return user.User.get_by_id(user_id)


# Import the views
import views
