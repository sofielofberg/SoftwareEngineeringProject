from dataclasses import dataclass

from user import User
from receipt import Receipt

@dataclass
class Admin (User):
    pass

    def rollback(self, receipt: Receipt):
        pass
