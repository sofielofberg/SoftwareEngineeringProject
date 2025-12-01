from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import db

if TYPE_CHECKING:
    from user import User


class Receipt(db.Model):
    __tablename__ = "receipt"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    submitter_id: Mapped[int] = mapped_column(ForeignKey("user.id"), init=False)
    submitter: Mapped[User] = relationship(foreign_keys=[submitter_id])
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

    handled_by: Mapped[User | None] = relationship(
        default=None, foreign_keys=[handled_by_id]
    )
    approved_by: Mapped[User | None] = relationship(
        default=None, foreign_keys=[approved_by_id]
    )

    @staticmethod
    def get_by_id(receipt_id: int) -> Receipt | None:
        return db.session.get(Receipt, receipt_id)

    @staticmethod
    def get_all() -> list[Receipt]:
        return db.session.scalars(select(Receipt)).all()

    def can_be_handled(self) -> bool:
        return not self.denied and self.handled_by is None

    def can_be_approved(self) -> bool:
        return (not self.denied and self.handled_by is not None
                and self.approved_by is None)

    def is_approved(self) -> bool:
        return self.approved_by is not None

    def can_be_denied(self) -> bool:
        return not self.denied and self.approved_by is None

    def set_handled_by(self, user: User):
        assert user.can_handle(self)
        assert self.handled_by is None
        self.handled_by = user
        self.save()

    def set_approved_by(self, user: User):
        assert user.can_approve(self)
        assert self.approved_by is None
        self.approved_by = user
        self.save()

    def set_as_denied(self, user: User):
        assert user.can_deny(self)
        assert not self.denied
        self.denied = True
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
