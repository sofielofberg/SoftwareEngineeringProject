from receipt import Receipt
from user import User

class Salesman(User):
    __mapper_args__ = {
        "polymorphic_identity": "salesman",
    }

    def submit(self, receipt: Receipt):
        pass

    def get_submitted_receipts(self) -> list[Receipt]:
        pass
