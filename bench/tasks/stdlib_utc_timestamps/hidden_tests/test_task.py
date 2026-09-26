import importlib
import time

import pytest

pytestmark = pytest.mark.filterwarnings("error::DeprecationWarning")


@pytest.fixture
def mod():
    return importlib.import_module("timefmt")


def test_iso(mod):
    assert mod.to_utc_iso(0) == "1970-01-01T00:00:00+00:00"
    assert mod.to_utc_iso(1700000000) == "2023-11-14T22:13:20+00:00"


def test_day_bucket(mod):
    assert mod.day_bucket(86399) == "1970-01-01"
    assert mod.day_bucket(86400) == "1970-01-02"


def test_seconds_until(mod):
    assert mod.seconds_until(time.time() + 100) == pytest.approx(100, abs=2)
    assert mod.seconds_until(time.time() - 50) == pytest.approx(-50, abs=2)
