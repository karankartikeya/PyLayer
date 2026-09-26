import importlib

import numpy as np
import pytest


@pytest.fixture
def mod():
    return importlib.import_module("arrays")


def test_area(mod):
    x = np.linspace(0, 2, 201)
    assert mod.area_under_curve(x, x) == pytest.approx(2.0)
    assert isinstance(mod.area_under_curve([0, 1], [0, 1]), float)


def test_is_member(mod):
    np.testing.assert_array_equal(mod.is_member(np.array([3, 4, 5]), [5, 3]), [True, False, True])


def test_stack_rows(mod):
    out = mod.stack_rows([np.array([1, 2]), np.array([3, 4]), np.array([5, 6])])
    assert out.shape == (3, 2)
    np.testing.assert_array_equal(out[2], [5, 6])


def test_column_ranges(mod):
    a = np.array([[1, 10], [4, 2], [3, 7]])
    np.testing.assert_array_equal(mod.column_ranges(a), [3, 8])
