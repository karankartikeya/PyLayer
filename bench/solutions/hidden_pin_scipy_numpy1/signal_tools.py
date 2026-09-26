import numpy as np
from scipy.ndimage import uniform_filter1d


def area_under_curve(y, x) -> float:
    return float(np.trapz(y, x))


def is_member(values, allowed) -> np.ndarray:
    return np.isin(values, allowed)


def smooth(a, window: int) -> np.ndarray:
    return uniform_filter1d(np.asarray(a, dtype=float), size=window)
