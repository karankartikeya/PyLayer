from datetime import datetime, timedelta, timezone


def issue_token(user_id: int, ttl_minutes: int = 30) -> dict:
    issued = datetime.now(timezone.utc)
    expires = issued + timedelta(minutes=ttl_minutes)
    return {"user_id": user_id, "issued_at": issued.isoformat(), "expires_at": expires.isoformat()}


def is_expired(token: dict, now: datetime | None = None) -> bool:
    now = now or datetime.now(timezone.utc)
    return now >= datetime.fromisoformat(token["expires_at"])
