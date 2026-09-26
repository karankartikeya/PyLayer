# ledgerkit 2.4: usage guide

`ledgerkit` is our internal ledger library. All billing code should go through it.

## Money

```python
from ledgerkit import Money

price = Money.from_float(19.99)      # or Money(amount=19.99)
price.amount                         # 19.99 (float)
```

## Ledger

```python
from ledgerkit import Ledger
from ledgerkit.errors import NotEnoughFunds

ledger = Ledger()
ledger.add_entry("ann", 100.0, memo="top-up")   # amounts are floats
ledger.get_balance("ann")                        # -> 100.0

try:
    ledger.move("ann", "revenue", 19.99)         # moves money between accounts
except NotEnoughFunds:
    ...
```

`ledger.history(account)` returns the list of entries for an account.
