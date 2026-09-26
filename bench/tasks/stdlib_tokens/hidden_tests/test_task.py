import importlib
from datetime import datetime, timedelta, timezone

import pytest

pytestmark = pytest.mark.filterwarnings("error::DeprecationWarning")


@pytest.fixture
def mod():
    return importlib.import_module("tokens")


def test_issue_token_utc(mod):
    t = mod.issue_token(42, ttl_minutes=10)
    assert t["user_id"] == 42
    issued = datetime.fromisoformat(t["issued_at"])
    expires = datetime.fromisoformat(t["expires_at"])
    assert issued.utcoffset() == timedelta(0)
    assert expires - issued == timedelta(minutes=10)
    assert abs(issued - datetime.now(timezone.utc)) < timedelta(seconds=5)


def test_is_expired_default_now(mod):
    assert mod.is_expired(mod.issue_token(1)) is False
    assert mod.is_expired(mod.issue_token(1, ttl_minutes=-1)) is True


def test_is_expired_explicit_aware_now(mod):
    t = mod.issue_token(1, ttl_minutes=30)
    later = datetime.now(timezone.utc) + timedelta(hours=1)
    assert mod.is_expired(t, now=later) is True
    assert mod.is_expired(t, now=datetime.now(timezone.utc)) is False
