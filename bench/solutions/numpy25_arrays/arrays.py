import numpy as np


def area_under_curve(y, x) -> float:
    return float(np.trapezoid(y, x))


def is_member(values, allowed) -> np.ndarray:
    return np.isin(values, allowed)


def stack_rows(rows: list) -> np.ndarray:
    return np.vstack(rows)


def column_ranges(a: np.ndarray) -> np.ndarray:
    return np.ptp(a, axis=0)
