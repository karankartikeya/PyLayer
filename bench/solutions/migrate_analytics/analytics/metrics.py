import numpy as np


def weighted_mean(values, weights):
    v = np.asarray(values, dtype=np.float64)
    w = np.asarray(weights, dtype=np.float64)
    return float(np.sum(v * w) / np.sum(w))


def clean(values):
    """Float copy with negative readings replaced by NaN."""
    a = np.array(values, dtype=np.float64)
    a[a < 0] = np.nan
    return a


def growth(rates):
    """Cumulative growth factor for a sequence of period rates (0.1 = +10%)."""
    return np.cumprod(1 + np.asarray(rates, dtype=np.float64))


def top_share(values, k):
    """Share of the total held by the k largest values, rounded to 4 places."""
    a = np.sort(np.asarray(values, dtype=np.float64))[::-1]
    return float(np.round(a[:k].sum() / a.sum(), 4))
