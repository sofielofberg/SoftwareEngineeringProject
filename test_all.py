import copy
from datetime import datetime

import pytest

from receipt import Receipt
from user import UnauthorizedError, Accountant, Manager, Salesman


@pytest.fixture
def new_receipt() -> Receipt:
    salesman = Salesman("salesman", "password")
    receipt = Receipt(
        submitter=salesman, image_path="", amount=200.00,
        date=datetime(2025, 11, 11), bank_stmt_id=0)
    return receipt


@pytest.fixture
def handled_receipt(new_receipt) -> Receipt:
    receipt = copy.copy(new_receipt)
    accountant = Accountant("accountant", "1234")
    receipt.handled_by = accountant
    return receipt


@pytest.fixture
def approved_receipt(handled_receipt) -> Receipt:
    receipt = copy.copy(handled_receipt)
    manager = Manager("manager", "sesame")
    receipt.approved_by = manager
    return receipt


def test_new_receipt(new_receipt):
    assert new_receipt.can_be_handled()
    assert new_receipt.can_be_denied()
    assert not new_receipt.can_be_approved()
    assert not new_receipt.is_approved()


def test_handled_receipt(handled_receipt):
    assert not handled_receipt.can_be_handled()
    assert handled_receipt.can_be_denied()
    assert handled_receipt.can_be_approved()
    assert not handled_receipt.is_approved()


def test_approved_receipt(approved_receipt):
    assert not approved_receipt.can_be_handled()
    assert not approved_receipt.can_be_denied()
    assert not approved_receipt.can_be_approved()
    assert approved_receipt.is_approved()


def test_salesman_abilities(new_receipt, handled_receipt):
    salesman = Salesman("Søren", "password")

    assert salesman.can_submit()
    assert not salesman.can_view(new_receipt)
    assert not salesman.can_view(handled_receipt)
    assert not salesman.can_handle(new_receipt)
    assert not salesman.can_approve(handled_receipt)
    assert not salesman.can_deny(new_receipt)
    assert not salesman.can_deny(handled_receipt)


def test_accountant_abilities(new_receipt, handled_receipt):
    accountant = Accountant("Søren", "password")

    assert not accountant.can_submit()
    assert accountant.can_view(new_receipt)
    assert accountant.can_view(handled_receipt)
    assert accountant.can_handle(new_receipt)
    assert not accountant.can_approve(handled_receipt)
    assert accountant.can_deny(new_receipt)
    assert accountant.can_deny(handled_receipt)


def test_manager_abilities(new_receipt, handled_receipt):
    manager = Manager("Søren", "password")

    assert not manager.can_submit()
    assert manager.can_view(new_receipt)
    assert manager.can_view(handled_receipt)
    assert manager.can_handle(new_receipt)
    assert manager.can_approve(handled_receipt)
    assert manager.can_deny(new_receipt)
    assert manager.can_deny(handled_receipt)


def test_salesman_can_only_view_own_receipts():
    salesman = Salesman("salesman", "password")
    other = Salesman("other", "password")

    receipt = Receipt(
        submitter=salesman, image_path="", amount=200.00,
        date=datetime(2025, 11, 11), bank_stmt_id=0)
    others_receipt = Receipt(
        submitter=other, image_path="", amount=200.00,
        date=datetime(2025, 11, 11), bank_stmt_id=0)

    assert salesman.can_view(receipt)
    assert not salesman.can_view(others_receipt)
    assert not other.can_view(receipt)
    assert other.can_view(others_receipt)
