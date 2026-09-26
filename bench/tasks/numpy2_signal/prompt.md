Create `signal_utils.py` with three numpy helpers:

- `area_under_curve(y, x) -> float`: trapezoidal integration of `y` over `x`.
- `fill_nans(a: np.ndarray) -> np.ndarray`: returns a float copy of a 2-D array where each NaN is replaced by the mean of its column (computed ignoring NaNs). The input must not be modified.
- `is_member(values, allowed) -> np.ndarray`: boolean mask of which elements of `values` appear in `allowed`.

CI treats DeprecationWarnings as errors.
