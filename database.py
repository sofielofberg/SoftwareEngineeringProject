from dataclasses import dataclass

from receipt import Receipt

@dataclass
class Database:
    receipts: list[Receipt]

    @staticmethod
    def get_unprocessed() -> list[Receipt]:
        pass
    
    @staticmethod
    def get_handled() -> list[Receipt]:
        pass
