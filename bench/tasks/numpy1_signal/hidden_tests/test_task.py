import importlib

import numpy as np
import pytest

pytestmark = pytest.mark.filterwarnings("error::DeprecationWarning")


@pytest.fixture
def mod():
    return importlib.import_module("signal_utils")


def test_area(mod):
    x = np.linspace(0, 1, 101)
    assert mod.area_under_curve(x ** 2, x) == pytest.approx(1 / 3, abs=1e-4)
    assert isinstance(mod.area_under_curve([0, 2], [0, 1]), float)
    assert mod.area_under_curve([0, 2], [0, 1]) == pytest.approx(1.0)


def test_fill_nans(mod):
    a = np.array([[1, np.nan], [3, 4], [np.nan, 8]])
    before = a.copy()
    out = mod.fill_nans(a)
    np.testing.assert_allclose(out, [[1, 6], [3, 4], [2, 8]])
    np.testing.assert_array_equal(np.isnan(a), np.isnan(before))
    assert out.dtype.kind == "f"


def test_fill_nans_int_input(mod):
    out = mod.fill_nans(np.array([[1, 2], [3, 4]]))
    assert out.dtype.kind == "f"
    np.testing.assert_allclose(out, [[1, 2], [3, 4]])


def test_is_member(mod):
    mask = mod.is_member(np.array([1, 5, 2, 9]), [2, 9, 10])
    np.testing.assert_array_equal(mask, [False, False, True, True])
    assert mask.dtype == bool
