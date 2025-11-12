from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any

from accountant import Accountant
from bankstmt import BankStmt
from manager import Manager
from salesman import Salesman


class State(Enum):
    UNPROCESSED = auto()
    HANDLED = auto()
    APPROVED = auto()
    DENIED = auto()


@dataclass
class Receipt:
    submitter: Salesman
    receipt: Any
    date: datetime
    amount: float
    bank_stmt: BankStmt
    state: State
    handled_by: Accountant | None
    approved_by: Manager | None

    @staticmethod
    def get_unproccessed() -> Receipt:
        pass

    @staticmethod
    def get_handled() -> Receipt:
        pass

    def handle(self, accountant: Accountant):
        if self.state != State.UNPROCESSED:
            # TODO is this the right thing?
            raise Exception(f"Cannot handle receipt in state: {self.state}")
        
        self.state = State.HANDLED
        self.handled_by = accountant
    
    def deny(self, accountant: Accountant):
        if self.state not in [State.UNPROCESSED, State.HANDLED]:
            raise Exception(f"Cannot deny receipt in state: {self.state}")
        
        self.state = State.DENIED

    def approve(self, manager: Manager):
        if self.state != State.HANDLED:
            raise Exception(f"Cannot approve receipt in state: {self.state}")
        
        self.state = State.DENIED
        self.approved_by = manager
