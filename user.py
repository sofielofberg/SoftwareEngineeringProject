from __future__ import annotations

from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column

from database import db
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
    def get_by_id(user_id: int) -> User | None:
        return db.session.get(User, user_id)

    @staticmethod
    def get_by_username(username: str) -> User | None:
        return db.session.scalar(select(User).filter_by(username=username))

    def can_submit(self) -> bool:
        return False

    def can_view(self, receipt: Receipt) -> bool:
        return False

    def can_handle(self, receipt: Receipt) -> bool:
        return False

    def can_approve(self, receipt: Receipt) -> bool:
        return False

    def can_deny(self, receipt: Receipt) -> bool:
        return False

    def submit(self, image_path: str, amount: float,
               date: datetime, bank_stmt_id: int) -> Receipt:
        if not self.can_submit():
            raise UnauthorizedError()
        receipt = Receipt(self, image_path, amount, date, bank_stmt_id)
        receipt.save()
        return receipt

    def handle(self, receipt: Receipt):
        assert receipt.can_be_handled()
        if not self.can_handle(receipt):
            raise UnauthorizedError()
        receipt.handled_by = self
        receipt.save()

    def approve(self, receipt: Receipt):
        assert receipt.can_be_approved()
        if not self.can_approve(receipt):
            raise UnauthorizedError()
        receipt.approved_by = self
        receipt.save()

    def deny(self, receipt: Receipt):
        assert receipt.can_be_denied()
        if not self.can_deny(receipt):
            raise UnauthorizedError()
        receipt.denied = True
        receipt.save()

    def save(self):
        db.session.add(self)
        db.session.commit()


class Salesman(User):
    __mapper_args__ = {
        "polymorphic_identity": "salesman",
    }

    def can_submit(self) -> bool:
        return True

    def can_view(self, receipt: Receipt) -> bool:
        return self == receipt.submitter


class Accountant(User):
    __mapper_args__ = {
        "polymorphic_identity": "accountant",
    }

    def can_view(self, receipt: Receipt) -> bool:
        return True

    def can_handle(self, receipt: Receipt) -> bool:
        return receipt.can_be_handled()

    def can_deny(self, receipt: Receipt) -> bool:
        return receipt.can_be_denied()


class Manager(Accountant):
    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }

    def can_approve(self, receipt: Receipt) -> bool:
        return receipt.can_be_approved() and receipt.handled_by != self
