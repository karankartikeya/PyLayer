Create `sales.py` with three pandas helpers for our orders DataFrame (columns: `timestamp` (datetime64), `department` (str), `customer` (str), `amount` (float), `quantity` (int)):

- `add_orders(df, rows: list[dict]) -> pd.DataFrame`: returns a new DataFrame with the rows appended and the index renumbered from 0.
- `department_means(df) -> pd.DataFrame`: the mean of every numeric column per `department`, indexed by department.
- `hourly_revenue(df) -> pd.Series`: total `amount` per hour based on `timestamp`, including hours with no orders as 0.

CI treats FutureWarnings and DeprecationWarnings as errors.
