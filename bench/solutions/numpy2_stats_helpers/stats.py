import numpy as np


def to_float_array(x) -> np.ndarray:
    return np.asarray(x, dtype=np.float64)


def safe_max(a) -> float:
    arr = np.asarray(a, dtype=np.float64)
    if arr.size == 0 or np.all(np.isnan(arr)):
        return -np.inf
    return float(np.nanmax(arr))


def running_product(a) -> np.ndarray:
    return np.cumprod(a)


def round_to(a, decimals: int) -> np.ndarray:
    return np.round(a, decimals)


def all_positive(a) -> bool:
    return bool(np.all(np.asarray(a) > 0))
