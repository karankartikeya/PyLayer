import numpy as np


def to_float_array(x) -> np.ndarray:
    return np.asfarray(x)


def safe_max(a) -> float:
    arr = np.asfarray(a)
    if arr.size == 0 or np.alltrue(np.isnan(arr)):
        return np.NINF
    return float(np.nanmax(arr))


def running_product(a) -> np.ndarray:
    return np.cumproduct(a)


def round_to(a, decimals: int) -> np.ndarray:
    return np.round_(a, decimals)


def all_positive(a) -> bool:
    return bool(np.alltrue(np.asarray(a) > 0))
