from ledgerkit import InsufficientFunds, Ledger, Money


class PaymentDeclined(Exception):
    pass


def charge_customer(ledger: Ledger, customer: str, amount: str) -> None:
    try:
        ledger.transfer(customer, "revenue", Money.parse(amount))
    except InsufficientFunds as e:
        raise PaymentDeclined(str(e)) from e


def customer_balance(ledger: Ledger, customer: str) -> str:
    return f"{ledger.balance(customer).to_decimal():.2f}"
