from dataclasses import dataclass

from user import User

@dataclass
class Accountant (User):
    pass

    @staticmethod
    def view_all() -> list:
        pass
