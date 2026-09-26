import importlib

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def mod():
    return importlib.import_module("ts")


def test_fill_gaps(mod):
    s = pd.Series([np.nan, 1.0, np.nan, 3.0], index=pd.date_range("2025-01-01", periods=4, freq="D"))
    assert list(mod.fill_gaps(s)) == [1.0, 1.0, 1.0, 3.0]


def test_monthly_totals(mod):
    s = pd.Series(1.0, index=pd.date_range("2025-01-30", periods=4, freq="D"))
    out = mod.monthly_totals(s)
    assert list(out.values) == [2.0, 2.0]
    assert list(out.index) == [pd.Timestamp("2025-01-31"), pd.Timestamp("2025-02-28")]


def test_per_minute_mean(mod):
    idx = pd.to_datetime(["2025-01-01 00:00:10", "2025-01-01 00:00:50", "2025-01-01 00:01:30"])
    out = mod.per_minute_mean(pd.Series([1.0, 3.0, 5.0], index=idx))
    assert list(out.values) == [2.0, 5.0]


def test_hourly_index(mod):
    idx = mod.hourly_index("2025-03-01 22:00", 3)
    assert list(idx) == [pd.Timestamp("2025-03-01 22:00"), pd.Timestamp("2025-03-01 23:00"), pd.Timestamp("2025-03-02 00:00")]
