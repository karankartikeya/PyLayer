import numpy as np
import pandas as pd
import pytest

from analytics import metrics, report


@pytest.fixture
def sales():
    return pd.DataFrame({
        "ts": pd.to_datetime(["2025-01-30", "2025-01-31", "2025-02-02", "2025-02-02"]),
        "region": ["eu", "us", "eu", "us"],
        "rep": ["ann", "bo", "cy", "di"],
        "amount": [10.0, 20.0, 30.0, 40.0],
        "units": [1, 2, 3, 4],
    })


def test_metrics():
    assert metrics.weighted_mean([1, 2, 3], [1, 1, 2]) == pytest.approx(2.25)
    assert np.isnan(metrics.clean([1, -1, 2])[1])
    np.testing.assert_allclose(metrics.growth([0.1, 0.1]), [1.1, 1.21])
    assert metrics.top_share([1, 2, 3, 4], 2) == 0.7


def test_add_rows(sales):
    out = report.add_rows(sales, [{"ts": pd.Timestamp("2025-02-03"), "region": "eu", "rep": "ed", "amount": 5.0, "units": 1}])
    assert len(out) == 5 and list(out.index) == [0, 1, 2, 3, 4]


def test_by_region(sales):
    out = report.by_region(sales)
    assert out.loc["eu", "amount"] == 20.0


def test_daily_and_monthly(sales):
    d = report.daily(sales)
    assert list(d.values) == [10.0, 20.0, 20.0, 70.0]
    m = report.monthly(sales)
    assert list(m.values) == [30.0, 70.0]


def test_flag_big(sales):
    report.flag_big(sales, 25)
    assert list(sales["big"]) == [False, False, True, True]
