import numpy as np
import pandas as pd
import pytest

from analytics import metrics, report

pytestmark = [pytest.mark.filterwarnings("error::DeprecationWarning"), pytest.mark.filterwarnings("error::FutureWarning")]


@pytest.fixture
def sales():
    return pd.DataFrame({
        "ts": pd.to_datetime(["2025-01-30", "2025-02-27"]),
        "region": ["eu", "eu"],
        "rep": ["ann", "bo"],
        "amount": [10.0, 20.0],
        "units": [1, 2],
    })


def test_monthly_labels_month_end(sales):
    m = report.monthly(sales)
    assert list(m.index) == [pd.Timestamp("2025-01-31"), pd.Timestamp("2025-02-28")]


def test_by_region_numeric_only(sales):
    out = report.by_region(sales)
    assert "rep" not in out.columns
    assert list(out.columns) == ["amount", "units"]


def test_clean_is_float64_copy():
    src = [1, -2, 3]
    out = metrics.clean(src)
    assert out.dtype == np.float64
    assert src == [1, -2, 3]


def test_flag_big_returns_same_frame(sales):
    assert report.flag_big(sales, 15) is sales
    assert list(sales["big"]) == [False, True]
