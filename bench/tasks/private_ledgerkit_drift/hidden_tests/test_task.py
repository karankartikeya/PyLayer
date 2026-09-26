import importlib

import pytest
from ledgerkit import Ledger, Money


@pytest.fixture
def mod():
    return importlib.import_module("billing")


@pytest.fixture
def ledger():
    lg = Ledger()
    lg.post("ann", Money.parse("100.00"), memo="top-up")
    return lg


def test_charge(mod, ledger):
    mod.charge_customer(ledger, "ann", "19.99")
    assert ledger.balance("ann") == Money.parse("80.01")
    assert ledger.balance("revenue") == Money.parse("19.99")
    assert mod.customer_balance(ledger, "ann") == "80.01"


def test_declined(mod, ledger):
    with pytest.raises(mod.PaymentDeclined):
        mod.charge_customer(ledger, "ann", "100.01")
    assert ledger.balance("ann") == Money.parse("100.00")


def test_exact_balance_and_zero(mod, ledger):
    mod.charge_customer(ledger, "ann", "100.00")
    assert mod.customer_balance(ledger, "ann") == "0.00"
    assert mod.customer_balance(ledger, "nobody") == "0.00"
