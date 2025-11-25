from __future__ import annotations

from typing import TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column

from database import db

if TYPE_CHECKING:
    from receipt import Receipt


class UnauthorizedError(Exception):
    pass


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

    def can_view(self, receipt: Receipt) -> bool:
        return False

    def can_handle(self, receipt: Receipt) -> bool:
        return False

    def can_approve(self, receipt: Receipt) -> bool:
        return False

    def can_deny(self, receipt: Receipt) -> bool:
        return False

    def handle(self, receipt: Receipt):
        raise UnauthorizedError()

    def approve(self, receipt: Receipt):
        raise UnauthorizedError()

    def deny(self, receipt: Receipt):
        raise UnauthorizedError()

    def save(self):
        db.session.add(self)
        db.session.commit()


class Salesman(User):
    __mapper_args__ = {
        "polymorphic_identity": "salesman",
    }

    def may_view(self, receipt):
        return self == receipt.submit

    def submit(self, receipt: Receipt):
        pass

    def get_submitted_receipts(self) -> list[Receipt]:
        pass


class Accountant(User):
    __mapper_args__ = {
        "polymorphic_identity": "accountant",
    }

    def can_view(self, receipt):
        return True

    def can_handle(self, receipt):
        return receipt.can_be_handled()

    def can_deny(self, receipt):
        return receipt.can_be_denied()

    def handle(self, receipt):
        assert receipt.can_be_handled()
        receipt.handled_by = self
        receipt.save()

    def deny(self, receipt):
        assert receipt.can_be_denied()
        receipt.denied = True
        receipt.save()


class Manager(Accountant):
    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }

    def can_approve(self, receipt):
        return receipt.can_be_approved() and receipt.handled_by != self

    def approve(self, receipt):
        assert receipt.can_be_approved()
        if receipt.handled_by == self:
            raise UnauthorizedError()

        receipt.approved_by = self
        receipt.save()
