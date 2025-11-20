from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    pass


db = SQLAlchemy(model_class=Base)


def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    db.init_app(app)


def setup_db(app):
    with app.app_context():
        import manager

        db.drop_all()
        db.create_all()
        db.session.add(manager.Manager("admin", "admin"))
        db.session.commit()
