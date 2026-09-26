import pandas as pd


def add_orders(df: pd.DataFrame, rows: list[dict]) -> pd.DataFrame:
    return df.append(rows, ignore_index=True)


def department_means(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("department").mean()


def hourly_revenue(df: pd.DataFrame) -> pd.Series:
    return df.set_index("timestamp")["amount"].resample("H").sum()
