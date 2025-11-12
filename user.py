from dataclasses import dataclass

@dataclass
class User:
    username: str
    password: str

    def login(self):
        pass
