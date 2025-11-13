from sqlalchemy.orm import Mapped, mapped_column

from main import db

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    type: Mapped[str] = mapped_column(init=False)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "user",
    }

    def login(self):
        pass

    def save_user(self):
        pass
