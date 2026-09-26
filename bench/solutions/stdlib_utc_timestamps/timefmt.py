import time
from datetime import datetime, timezone


def to_utc_iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def day_bucket(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")


def seconds_until(ts: float) -> float:
    return ts - time.time()
