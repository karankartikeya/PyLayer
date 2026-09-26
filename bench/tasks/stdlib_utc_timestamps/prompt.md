Create `timefmt.py` (standard library only):

- `to_utc_iso(ts: float) -> str`: converts a Unix timestamp to an ISO 8601 UTC string like `1970-01-01T00:00:00+00:00`.
- `day_bucket(ts: float) -> str`: the UTC calendar date of the timestamp as `YYYY-MM-DD`.
- `seconds_until(ts: float) -> float`: seconds from now until `ts` (negative if it's in the past).

We target Python 3.12 and CI treats DeprecationWarnings as errors.
