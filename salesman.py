from dataclasses import dataclass

from receipt import Receipt
from user import User

@dataclass
class Salesman (User):
    receipts: list[Receipt]
