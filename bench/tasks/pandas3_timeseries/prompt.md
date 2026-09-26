Create `ts.py` with helpers for sensor readings stored as a pandas Series with a DatetimeIndex:

- `fill_gaps(s) -> pd.Series`: forward-fill missing values, then back-fill any leading gaps.
- `monthly_totals(s) -> pd.Series`: sum per calendar month, labelled by the month-end date.
- `per_minute_mean(s) -> pd.Series`: mean per minute.
- `hourly_index(start: str, hours: int) -> pd.DatetimeIndex`: `hours` hourly timestamps starting at `start`.
