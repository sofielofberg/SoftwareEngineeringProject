from __future__ import annotations

from flask_login import UserMixin
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column

from database import db


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    type: Mapped[str] = mapped_column(init=False)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "user",
    }

    @staticmethod
    def get_by_id(user_id) -> User:
        return db.session.get(User, user_id)

    @staticmethod
    def get_by_username(username) -> User | None:
        return db.session.scalar(select(User).filter_by(username=username))

    def login(self):
        pass

    def save(self):
        db.session.add(self)
        db.session.commit()
