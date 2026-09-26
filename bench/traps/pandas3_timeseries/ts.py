import pandas as pd


def fill_gaps(s: pd.Series) -> pd.Series:
    return s.fillna(method="ffill").fillna(method="bfill")


def monthly_totals(s: pd.Series) -> pd.Series:
    return s.resample("M").sum()


def per_minute_mean(s: pd.Series) -> pd.Series:
    return s.resample("T").mean()


def hourly_index(start: str, hours: int) -> pd.DatetimeIndex:
    return pd.date_range(start, periods=hours, freq="H")
