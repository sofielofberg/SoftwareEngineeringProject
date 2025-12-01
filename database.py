from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    pass


db = SQLAlchemy(model_class=Base)


def init_db(app, db_connection):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_connection
    db.init_app(app)


def setup_db(app):
    with app.app_context():
        db.create_all()
