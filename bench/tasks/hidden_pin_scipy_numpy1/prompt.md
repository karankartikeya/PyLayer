Create `signal_tools.py` with:

- `area_under_curve(y, x) -> float`: trapezoidal integration of `y` over `x` using numpy.
- `is_member(values, allowed) -> np.ndarray`: boolean mask of which elements of `values` appear in `allowed`.
- `smooth(a, window: int) -> np.ndarray`: a moving average of a 1-D array with the given window, same length as the input, using scipy.
