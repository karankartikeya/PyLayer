import numpy as np


def area_under_curve(y, x) -> float:
    return float(np.trapz(y, x))


def fill_nans(a: np.ndarray) -> np.ndarray:
    out = np.array(a, dtype=float, copy=True)
    col_means = np.nanmean(out, axis=0)
    rows, cols = np.where(np.isnan(out))
    out[rows, cols] = col_means[cols]
    return out


def is_member(values, allowed) -> np.ndarray:
    return np.isin(values, allowed)
