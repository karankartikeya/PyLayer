import pandas as pd


def text_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if df[c].dtype == object]


def strip_all(df: pd.DataFrame) -> pd.DataFrame:
    return df.applymap(lambda v: v.strip() if isinstance(v, str) else v)


def first_days(df: pd.DataFrame, n: int) -> pd.DataFrame:
    return df.first(f"{n}D")


def void_cancelled(df: pd.DataFrame) -> None:
    df["amount"][df["status"] == "cancelled"] = 0.0
