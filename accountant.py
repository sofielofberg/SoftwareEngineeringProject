from user import User

class Accountant(User):
    __mapper_args__ = {
        "polymorphic_identity": "accountant",
    }
