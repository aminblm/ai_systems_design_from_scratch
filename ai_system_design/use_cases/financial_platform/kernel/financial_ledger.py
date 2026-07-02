
"""Financial Ledger Immutable source of truth for all financial state."""

import time, uuid

class LedgerEntry:
    def __init__(self, debit_account, credit_account, amount):
        self.id = uuid.uuid4().hex
        self.timestamp = time.time()
        self.debit = debit_account
        self.credit = credit_account
        self.amount = amount


class FinancialLedger:
    """Immutable source of truth for all financial state."""
    def __init__(self):
        self._entries = []

    def record(self, debit, credit, amount):
        """Append-only transaction registration."""
        entry = LedgerEntry(debit, credit, amount)
        self._entries.append(entry)
        return entry.id 
    
    def get_balance(self, account_name):
        """Calculates balance from ledger history."""
        balance = 0
        for entry in self._entries:
            if entry.debit == account_name: balance -= entry.amount
            if entry.credit == account_name: balance += entry.amount
        return balance