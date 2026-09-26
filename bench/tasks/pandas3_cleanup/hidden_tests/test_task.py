import importlib

import pandas as pd
import pytest

pytestmark = [
    pytest.mark.filterwarnings("error::DeprecationWarning"),
    pytest.mark.filterwarnings("error::FutureWarning"),
]


@pytest.fixture
def mod():
    return importlib.import_module("cleanup")


@pytest.fixture
def df():
    idx = pd.to_datetime(["2025-01-01 08:00", "2025-01-01 17:00", "2025-01-02 09:00",
                          "2025-01-03 23:00", "2025-01-04 12:00"])
    return pd.DataFrame({
        "status": ["paid", "cancelled ", "cancelled", "paid", "cancelled"],
        "customer": ["  ann", "bo ", " cy ", "di", "ed"],
        "amount": [10.0, 20.0, 30.0, 40.0, 50.0],
        "qty": [1, 2, 3, 4, 5],
    }, index=idx)


def test_text_columns(mod, df):
    assert mod.text_columns(df) == ["status", "customer"]


def test_strip_all(mod, df):
    out = mod.strip_all(df)
    assert list(out["customer"]) == ["ann", "bo", "cy", "di", "ed"]
    assert list(out["status"]) == ["paid", "cancelled", "cancelled", "paid", "cancelled"]
    assert list(out["amount"]) == [10.0, 20.0, 30.0, 40.0, 50.0]
    assert df["customer"].iloc[0] == "  ann"


def test_first_days(mod, df):
    assert len(mod.first_days(df, 2)) == 3
    assert len(mod.first_days(df, 3)) == 4


def test_void_cancelled_in_place(mod, df):
    assert mod.void_cancelled(df) is None
    assert list(df["amount"]) == [10.0, 20.0, 0.0, 40.0, 0.0]
