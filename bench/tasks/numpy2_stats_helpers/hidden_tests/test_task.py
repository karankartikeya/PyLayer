import importlib
import math

import numpy as np
import pytest


@pytest.fixture
def mod():
    return importlib.import_module("stats")


def test_to_float_array(mod):
    a = mod.to_float_array([[1, 2], [3, 4]])
    assert a.dtype == np.float64 and a.shape == (2, 2)


def test_safe_max(mod):
    assert mod.safe_max([1.0, np.nan, 3.0]) == 3.0
    assert mod.safe_max([]) == -math.inf
    assert mod.safe_max([np.nan, np.nan]) == -math.inf


def test_running_product(mod):
    np.testing.assert_allclose(mod.running_product([1, 2, 3, 4]), [1, 2, 6, 24])


def test_round_to(mod):
    np.testing.assert_allclose(mod.round_to([1.234, 5.678], 1), [1.2, 5.7])


def test_all_positive(mod):
    assert mod.all_positive([1, 2, 3]) is True
    assert mod.all_positive([1, 0, 3]) is False
