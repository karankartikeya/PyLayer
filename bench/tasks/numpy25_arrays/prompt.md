Create `arrays.py` with these numpy helpers:

- `area_under_curve(y, x) -> float`: trapezoidal integration of `y` over `x`.
- `is_member(values, allowed) -> np.ndarray`: boolean mask of which elements of `values` appear in `allowed`.
- `stack_rows(rows: list) -> np.ndarray`: stacks a list of equal-length 1-D arrays as the rows of a 2-D array.
- `column_ranges(a: np.ndarray) -> np.ndarray`: for a 2-D array, max minus min of each column.
