def run_query(engine, sql: str, params: dict | None = None) -> list[dict]:
    result = engine.execute(sql, params or {})
    return [dict(row) for row in result]


def table_counts(engine, tables: list[str]) -> dict[str, int]:
    return {t: engine.execute(f"SELECT COUNT(*) FROM {t}").scalar() for t in tables}
