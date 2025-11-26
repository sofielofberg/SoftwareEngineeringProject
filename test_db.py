from datetime import datetime

import pytest
from flask import Flask

from database import db, init_db, setup_db
from receipt import Receipt
from user import User, Salesman, Accountant, Manager


@pytest.fixture
def new_db():
    app = Flask("test")
    app.testing = True
    init_db(app, "sqlite://")
    setup_db(app)
    with app.app_context():
        yield db


def test_receipt(new_db):
    submitter = Salesman("Frank", "1234")
    submitter.save()
    receipt = Receipt(submitter, "", 100, datetime(2025, 10, 12), 0)
    receipt.save()

    assert Receipt.get_by_id(receipt.id) is not None
    assert receipt in Receipt.get_all()


def test_user(new_db):
    users = [Salesman("Egon", "1234"),
             Accountant("Benny", "kodeord"),
             Manager("Keld", "sesam sesam")]

    for user in users:
        user.save()

    for user in users:
        assert User.get_by_id(user.id) is user
        assert User.get_by_username(user.username) is user
