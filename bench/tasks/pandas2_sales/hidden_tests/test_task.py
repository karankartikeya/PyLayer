import importlib

import pandas as pd
import pytest

pytestmark = [
    pytest.mark.filterwarnings("error::FutureWarning"),
    pytest.mark.filterwarnings("error::DeprecationWarning"),
]


@pytest.fixture
def mod():
    return importlib.import_module("sales")


@pytest.fixture
def df():
    return pd.DataFrame({
        "timestamp": pd.to_datetime(["2024-01-01 09:10", "2024-01-01 09:50", "2024-01-01 11:05", "2024-01-01 11:30"]),
        "department": ["toys", "books", "toys", "books"],
        "customer": ["ann", "bo", "cy", "di"],
        "amount": [10.0, 20.0, 30.0, 40.0],
        "quantity": [1, 2, 3, 4],
    })


def test_add_orders(mod, df):
    rows = [{"timestamp": pd.Timestamp("2024-01-01 12:00"), "department": "toys",
             "customer": "ed", "amount": 5.0, "quantity": 1}]
    out = mod.add_orders(df, rows)
    assert len(out) == 5 and len(df) == 4
    assert list(out.index) == [0, 1, 2, 3, 4]
    assert out.iloc[-1]["customer"] == "ed"


def test_department_means(mod, df):
    out = mod.department_means(df)
    assert "customer" not in out.columns
    assert out.loc["toys", "amount"] == pytest.approx(20.0)
    assert out.loc["books", "quantity"] == pytest.approx(3.0)


def test_hourly_revenue(mod, df):
    s = mod.hourly_revenue(df)
    assert list(s.values) == [30.0, 0.0, 70.0]
    assert list(s.index) == list(pd.date_range("2024-01-01 09:00", periods=3, freq="h"))
