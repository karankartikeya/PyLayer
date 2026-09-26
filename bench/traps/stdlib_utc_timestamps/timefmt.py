from datetime import datetime


def to_utc_iso(ts: float) -> str:
    return datetime.utcfromtimestamp(ts).isoformat() + "+00:00"


def day_bucket(ts: float) -> str:
    return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")


def seconds_until(ts: float) -> float:
    return (datetime.utcfromtimestamp(ts) - datetime.utcnow()).total_seconds()
