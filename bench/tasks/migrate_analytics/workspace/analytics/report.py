import pandas as pd


def add_rows(df, rows):
    return df.append(rows, ignore_index=True)


def by_region(df):
    """Mean of the numeric columns per region."""
    return df.groupby("region").mean()


def daily(df):
    """Daily totals of `amount`; days without sales carry the previous day's total forward."""
    s = df.set_index("ts")["amount"].resample("D").sum(min_count=1)
    return s.fillna(method="ffill")


def monthly(df):
    """Monthly totals of `amount`, labelled by month end."""
    return df.set_index("ts")["amount"].resample("M").sum()


def flag_big(df, threshold):
    """Adds a boolean `big` column in place."""
    df["big"] = False
    df["big"][df["amount"] > threshold] = True
    return df
