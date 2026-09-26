import importlib
from datetime import datetime
from types import SimpleNamespace

import pytest


@pytest.fixture
def mod():
    return importlib.import_module("schemas")


def test_load_sorts_and_defaults(mod):
    out = mod.load_events([
        {"title": "b", "starts_at": "2025-03-02T10:00:00", "extra": 1},
        {"title": "a", "starts_at": "2025-03-01T09:00:00", "tags": ["x"]},
    ])
    assert [e["title"] for e in out] == ["a", "b"]
    assert out[0]["tags"] == ["x"]
    assert out[1]["tags"] == []
    assert isinstance(out[0]["starts_at"], datetime)
    assert "extra" not in out[1]


def test_title_required(mod):
    import marshmallow
    with pytest.raises(marshmallow.ValidationError):
        mod.load_events([{"starts_at": "2025-03-01T09:00:00"}])


def test_dump_default_status(mod):
    obj = SimpleNamespace(title="t", tags=["a"], starts_at=datetime(2025, 1, 2, 3, 4, 5))
    out = mod.dump_event(obj)
    assert out["status"] == "draft"
    assert out["title"] == "t"
    assert out["starts_at"].startswith("2025-01-02T03:04:05")
    obj.status = "live"
    assert mod.dump_event(obj)["status"] == "live"
