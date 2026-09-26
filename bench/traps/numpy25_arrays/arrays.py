import numpy as np


def area_under_curve(y, x) -> float:
    return float(np.trapz(y, x))


def is_member(values, allowed) -> np.ndarray:
    return np.in1d(values, allowed)


def stack_rows(rows: list) -> np.ndarray:
    return np.row_stack(rows)


def column_ranges(a: np.ndarray) -> np.ndarray:
    return a.ptp(axis=0)
