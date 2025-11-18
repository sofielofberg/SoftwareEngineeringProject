from user import User
from receipt import Receipt

class Admin(User):
    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

    def rollback(self, receipt: Receipt):
        pass

