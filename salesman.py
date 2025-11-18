from __future__ import annotations

import receipt
from user import User


class Salesman(User):
    __mapper_args__ = {
        "polymorphic_identity": "salesman",
    }

    def submit(self, receipt: receipt.Receipt):
        pass

    def get_submitted_receipts(self) -> list[receipt.Receipt]:
        pass

