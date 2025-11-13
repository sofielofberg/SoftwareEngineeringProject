from accountant import Accountant

class Manager(Accountant):
    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }
