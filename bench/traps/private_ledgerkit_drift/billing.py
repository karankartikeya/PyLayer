from ledgerkit import Ledger, Money
from ledgerkit.errors import NotEnoughFunds


class PaymentDeclined(Exception):
    pass


def charge_customer(ledger: Ledger, customer: str, amount: str) -> None:
    try:
        ledger.move(customer, "revenue", Money.from_float(float(amount)).amount)
    except NotEnoughFunds as e:
        raise PaymentDeclined(str(e)) from e


def customer_balance(ledger: Ledger, customer: str) -> str:
    return f"{ledger.get_balance(customer):.2f}"
