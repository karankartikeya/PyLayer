from __future__ import annotations

from dataclasses import dataclass

from ledgerkit.money import Money


class InsufficientFunds(Exception):
    pass


@dataclass(frozen=True)
class Entry:
    account: str
    amount: Money
    memo: str = ""


class Ledger:
    def __init__(self, currency: str = "USD") -> None:
        self.currency = currency
        self._entries: list[Entry] = []

    def post(self, account: str, amount: Money, *, memo: str = "") -> Entry:
        """Record a single entry (positive = credit to the account)."""
        if not isinstance(amount, Money):
            raise TypeError(f"amount must be Money, got {type(amount).__name__}")
        entry = Entry(account, amount, memo)
        self._entries.append(entry)
        return entry

    def balance(self, account: str) -> Money:
        total = Money.zero(self.currency)
        for e in self._entries:
            if e.account == account:
                total = total + e.amount
        return total

    def transfer(self, source: str, dest: str, amount: Money, *, memo: str = "") -> None:
        """Move money between accounts. Raises InsufficientFunds if source would go negative."""
        if not isinstance(amount, Money):
            raise TypeError(f"amount must be Money, got {type(amount).__name__}")
        if self.balance(source) < amount:
            raise InsufficientFunds(f"{source} has {self.balance(source)}, needs {amount}")
        self.post(source, -amount, memo=memo)
        self.post(dest, amount, memo=memo)

    def entries(self, account: str | None = None) -> list[Entry]:
        return [e for e in self._entries if account is None or e.account == account]
