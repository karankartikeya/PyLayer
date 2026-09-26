from sqlalchemy import text


def run_query(engine, sql: str, params: dict | None = None) -> list[dict]:
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return [dict(row._mapping) for row in result]


def table_counts(engine, tables: list[str]) -> dict[str, int]:
    counts = {}
    with engine.connect() as conn:
        for table in tables:
            counts[table] = conn.execute(text(f'SELECT COUNT(*) FROM "{table}"')).scalar_one()
    return counts
