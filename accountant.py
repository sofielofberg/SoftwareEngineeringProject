from user import User


class Accountant(User):
    __mapper_args__ = {
        "polymorphic_identity": "accountant",
    }

    def can_view(self, receipt):
        return True

    def can_handle(self, receipt):
        return receipt.can_be_handled()

    def can_deny(self, receipt):
        return receipt.can_be_denied()

    def handle(self, receipt):
        assert receipt.can_be_handled()
        receipt.handled_by = self
        receipt.save()

    def deny(self, receipt):
        assert receipt.can_be_denied()
        receipt.denied = True
        receipt.save()
