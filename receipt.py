from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime, Double

from main import db
from accountant import Accountant
from manager import Manager


class Receipt(db.Model):
    __tablename__ = "receipt"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    submitter_id: Mapped[int] = mapped_column(ForeignKey("salesmen.id"))
    image_path: Mapped[str]
    date: DateTime
    amount: Double
    bank_stmt_id: Mapped[int]

    denied: Mapped[bool] = mapped_column(default=False)
    handled_by: Mapped[Optional[int]] = mapped_column(ForeignKey("accountant.id"), default=None)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("manager.id"), default=None)

    @staticmethod
    def get_unprocessed() -> list[Receipt]:
        pass

    @staticmethod
    def get_handled() -> list[Receipt]:
        pass

    @staticmethod
    def get_all() -> list[Receipt]:
        pass

    def is_unprocessed(self) -> bool:
        return self.handled_by == None and self.approved_by == None and self.denied == False

    def is_approved(self) -> bool:
        return self.approved_by != None

    def is_handled(self) -> bool:
        return self.handled_by != None

    def handle(self, accountant: Accountant):
        if self.is_unprocessed():
            # TODO is this the right thing?
            raise Exception(f"Cannot handle receipt in state: {self.state}")

        self.handled_by = accountant

    def deny(self, accountant: Accountant):
        if not self.is_approved():
            raise Exception(f"Cannot deny receipt in state: {self.state}")

        self.deny = False

    def approve(self, manager: Manager):
        if not self.is_handled():
            raise Exception(f"Cannot approve receipt in state: {self.state}")

        self.approved_by = manager
