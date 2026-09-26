import importlib

import numpy as np
import pytest


@pytest.fixture
def mod():
    return importlib.import_module("signal_tools")


def test_area(mod):
    x = np.linspace(0, 1, 11)
    assert mod.area_under_curve(2 * x, x) == pytest.approx(1.0)
    assert isinstance(mod.area_under_curve([0, 1], [0, 1]), float)


def test_is_member(mod):
    np.testing.assert_array_equal(mod.is_member([1, 2, 3], [3, 1]), [True, False, True])


def test_smooth(mod):
    out = mod.smooth(np.array([0.0, 0.0, 3.0, 0.0, 0.0]), 3)
    assert out.shape == (5,)
    assert out[2] == pytest.approx(1.0)
    assert out[1] == pytest.approx(1.0) and out[3] == pytest.approx(1.0)
