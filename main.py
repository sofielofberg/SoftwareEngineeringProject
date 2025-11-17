# Setup inspired by
# https://flask.palletsprojects.com/en/stable/patterns/packages/

from flask import Flask
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


from receipt import Receipt

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()

# Import the views
import views
