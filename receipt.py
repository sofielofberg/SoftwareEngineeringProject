from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

import salesman
from accountant import Accountant
from database import db
from manager import Manager


class Receipt(db.Model):
    __tablename__ = "receipt"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    submitter_id: Mapped[int] = mapped_column(ForeignKey("user.id"), init=False)
    submitter: Mapped[salesman.Salesman] = relationship(
        foreign_keys=[submitter_id]
    )
    image_path: Mapped[str]
    amount: Mapped[float]
    date: Mapped[datetime]
    bank_stmt_id: Mapped[int]

    denied: Mapped[bool] = mapped_column(default=False)
    handled_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.id"), default=None
    )
    approved_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.id"), default=None
    )

    handled_by: Mapped[Accountant | None] = relationship(
        default=None, foreign_keys=[handled_by_id]
    )
    approved_by: Mapped[Manager | None] = relationship(
        default=None, foreign_keys=[approved_by_id]
    )

    @staticmethod
    def get_by_id(receipt_id: int) -> Receipt | None:
        return db.session.get(Receipt, receipt_id)

    @staticmethod
    def get_unprocessed() -> list[Receipt]:
        return db.session.scalars(select(Receipt)).filter_by(
            handled_by=None, approved_by=None, denied=False
        )

    @staticmethod
    def get_handled() -> list[Receipt]:
        return db.session.scalars(select(Receipt)).where(
            Receipt.handled_by is not None and not Receipt.denied
        )

    @staticmethod
    def get_all() -> list[Receipt]:
        return db.session.scalars(select(Receipt)).all()

    def can_be_handled(self) -> bool:
        return not self.denied and self.handled_by is None

    def can_be_approved(self) -> bool:
        return (not self.denied and self.handled_by is not None
                and self.approved_by is None)

    def can_be_denied(self) -> bool:
        return not self.denied and self.approved_by is None

    def save(self):
        db.session.add(self)
        db.session.commit()
