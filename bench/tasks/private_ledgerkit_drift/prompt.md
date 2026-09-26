Our billing code uses our internal `ledgerkit` library (it's already installed in the project venv; there's a usage guide in docs/ledgerkit.md).

Create `billing.py` with:

- a `PaymentDeclined` exception
- `charge_customer(ledger, customer: str, amount: str) -> None`: move `amount` (a decimal string like `"19.99"`) from the customer's account to the `"revenue"` account; raise `PaymentDeclined` if the customer doesn't have enough funds.
- `customer_balance(ledger, customer: str) -> str`: the customer's balance as a plain decimal string like `"80.01"`.
