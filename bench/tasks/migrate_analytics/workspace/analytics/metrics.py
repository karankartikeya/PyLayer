import numpy as np


def weighted_mean(values, weights):
    v = np.asfarray(values)
    w = np.asfarray(weights)
    return float(np.sum(v * w) / np.sum(w))


def clean(values):
    """Float copy with negative readings replaced by NaN."""
    a = np.array(values, dtype=np.float_)
    a[a < 0] = np.NaN
    return a


def growth(rates):
    """Cumulative growth factor for a sequence of period rates (0.1 = +10%)."""
    return np.cumproduct(1 + np.asfarray(rates))


def top_share(values, k):
    """Share of the total held by the k largest values, rounded to 4 places."""
    a = np.sort(np.asfarray(values))[::-1]
    return float(np.round_(a[:k].sum() / a.sum(), 4))
