"""ledgerkit: double-entry style ledger with integer-cent money (internal package).

3.0 breaking changes: Money is cent-based (Money.parse / Money(cents=...)); Ledger.add_entry -> post,
Ledger.move -> transfer, Ledger.get_balance -> balance (returns Money); errors live in ledgerkit.ledger.
"""

from ledgerkit.ledger import Entry, InsufficientFunds, Ledger
from ledgerkit.money import CurrencyMismatch, Money

__version__ = "3.0.0"
__all__ = ["Entry", "InsufficientFunds", "Ledger", "Money", "CurrencyMismatch"]
