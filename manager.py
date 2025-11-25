from accountant import Accountant
from user import UnauthorizedError


class Manager(Accountant):
    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }

    def can_approve(self, receipt):
        return receipt.can_be_approved() and receipt.handled_by != self

    def approve(self, receipt):
        assert receipt.can_be_approved()
        if receipt.handled_by == self:
            raise UnauthorizedError()

        receipt.approved_by = self
        receipt.save()
