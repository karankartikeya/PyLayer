Create `tokens.py` (standard library only) with:

- `issue_token(user_id: int, ttl_minutes: int = 30) -> dict` returning `{"user_id": ..., "issued_at": ..., "expires_at": ...}`, where both timestamps are ISO 8601 strings in UTC.
- `is_expired(token: dict, now: datetime | None = None) -> bool`, defaulting `now` to the current time.

We target Python 3.12 and CI treats DeprecationWarnings as errors.
