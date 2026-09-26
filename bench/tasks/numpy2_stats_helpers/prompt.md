Create `stats.py` with these numpy helpers:

- `to_float_array(x) -> np.ndarray`: converts any array-like (lists, ints, nested lists) to a float64 array.
- `safe_max(a) -> float`: the maximum ignoring NaNs; negative infinity for an empty or all-NaN input.
- `running_product(a) -> np.ndarray`: cumulative product.
- `round_to(a, decimals: int) -> np.ndarray`: elementwise rounding.
- `all_positive(a) -> bool`: whether every element is > 0.
