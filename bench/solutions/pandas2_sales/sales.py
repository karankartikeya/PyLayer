import pandas as pd


def add_orders(df: pd.DataFrame, rows: list[dict]) -> pd.DataFrame:
    return pd.concat([df, pd.DataFrame(rows)], ignore_index=True)


def department_means(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("department").mean(numeric_only=True)


def hourly_revenue(df: pd.DataFrame) -> pd.Series:
    return df.set_index("timestamp")["amount"].resample("h").sum()
