from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

import salesman
from main import db
from accountant import Accountant
from manager import Manager


class Receipt(db.Model):
    __tablename__ = "receipt"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    submitter_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    image_path: Mapped[str]
    date: Mapped[datetime]
    amount: Mapped[float]
    bank_stmt_id: Mapped[int]
    state: Mapped[str]

    denied: Mapped[bool] = mapped_column(default=False)
    handled_by_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"), default=None)
    approved_by_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"), default=None)

    submitter: Mapped[salesman.Salesman] = relationship(init=False)
    handled_by: Mapped[Accountant | None] = relationship(default=None)
    approved_by: Mapped[Manager | None] = relationship(default=None)

    @staticmethod
    def get_unprocessed() -> list[Receipt]:
        return db.session.scalars(select(Receipt)).filter_by(
            handled_by=None, approved_by=None, denied=False
        )

    @staticmethod
    def get_handled() -> list[Receipt]:
        return db.session.scalars(select(Receipt)).where(
            Receipt.handled_by != None and not Receipt.denied
        )

    @staticmethod
    def get_all() -> list[Receipt]:
        return db.session.scalars(select(Receipt)).all()

    def is_unprocessed(self) -> bool:
        return self.handled_by == None and self.approved_by == None and not self.denied

    def is_approved(self) -> bool:
        return self.approved_by != None and not self.denied

    def is_handled(self) -> bool:
        return self.handled_by != None and not self.denied

    def handle(self, accountant: Accountant):
        assert isinstance(accountant, Accountant)

        if self.is_unprocessed():
            # TODO is this the right thing?
            raise Exception(f"Cannot handle receipt in state: {self.state}")

        self.handled_by = accountant

    def deny(self, accountant: Accountant):
        assert isinstance(accountant, Accountant)

        if not self.is_approved():
            raise Exception(f"Cannot deny receipt in state: {self.state}")

        self.deny = False

    def approve(self, manager: Manager):
        assert isinstance(manager, Manager)

        if not self.is_handled():
            raise Exception(f"Cannot approve receipt in state: {self.state}")

        if self.handled_by == Manager:
            raise Exception("Cannot be approved by same manager that handled receipt")

        self.approved_by = manager
