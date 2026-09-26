Create `cleanup.py` with helpers for our orders DataFrame. It has a DatetimeIndex and columns `status` (text), `customer` (text), `amount` (float) and `qty` (int).

- `text_columns(df) -> list[str]`: names of the columns that hold text, in column order.
- `strip_all(df) -> pd.DataFrame`: a new DataFrame with leading/trailing whitespace stripped from every text cell; other cells unchanged.
- `first_days(df, n: int) -> pd.DataFrame`: the rows falling within the first `n` days of the data.
- `void_cancelled(df) -> None`: in place, set `amount` to 0 for rows whose `status` is `"cancelled"`.

CI treats DeprecationWarnings and FutureWarnings as errors.
