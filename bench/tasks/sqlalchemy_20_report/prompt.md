Create `report.py` with two helpers for ad-hoc reporting against a SQLAlchemy engine:

- `run_query(engine, sql: str, params: dict | None = None) -> list[dict]` executes a raw SQL string with named parameters (`:name` style) and returns each row as a plain dict of column name to value.
- `table_counts(engine, tables: list[str]) -> dict[str, int]` returns the number of rows in each table.
