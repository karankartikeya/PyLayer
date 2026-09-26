import pandas as pd


def text_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if pd.api.types.is_string_dtype(df[c])]


def strip_all(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in text_columns(out):
        out[c] = out[c].str.strip()
    return out


def first_days(df: pd.DataFrame, n: int) -> pd.DataFrame:
    start = df.index.min().normalize()
    return df[df.index < start + pd.Timedelta(days=n)]


def void_cancelled(df: pd.DataFrame) -> None:
    df.loc[df["status"] == "cancelled", "amount"] = 0.0
