from datetime import datetime, timedelta


def issue_token(user_id: int, ttl_minutes: int = 30) -> dict:
    issued = datetime.utcnow()
    expires = issued + timedelta(minutes=ttl_minutes)
    return {"user_id": user_id, "issued_at": issued.isoformat() + "Z", "expires_at": expires.isoformat() + "Z"}


def is_expired(token: dict, now: datetime | None = None) -> bool:
    now = now or datetime.utcnow()
    return now >= datetime.fromisoformat(token["expires_at"].rstrip("Z"))
