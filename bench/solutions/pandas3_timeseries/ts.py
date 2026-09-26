import pandas as pd


def fill_gaps(s: pd.Series) -> pd.Series:
    return s.ffill().bfill()


def monthly_totals(s: pd.Series) -> pd.Series:
    return s.resample("ME").sum()


def per_minute_mean(s: pd.Series) -> pd.Series:
    return s.resample("min").mean()


def hourly_index(start: str, hours: int) -> pd.DatetimeIndex:
    return pd.date_range(start, periods=hours, freq="h")
