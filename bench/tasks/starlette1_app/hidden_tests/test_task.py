import importlib

import pytest
from starlette.testclient import TestClient


@pytest.fixture
def mod():
    return importlib.import_module("app")


def test_hits(mod):
    with TestClient(mod.app) as c:
        assert c.get("/hit").json() == {"hits": 1}
        assert c.get("/hit").json() == {"hits": 2}


def test_keyerror_handler(mod):
    with TestClient(mod.app, raise_server_exceptions=False) as c:
        r = c.get("/boom")
        assert r.status_code == 404
        assert r.json() == {"error": "not found"}


def test_lifecycle_uses_hooks(mod, monkeypatch):
    seen = {}
    monkeypatch.setattr(mod, "open_store", lambda: {"hits": 41})
    monkeypatch.setattr(mod, "close_store", lambda store: seen.setdefault("closed", store))
    with TestClient(mod.app) as c:
        assert c.get("/hit").json() == {"hits": 42}
    assert seen["closed"]["hits"] == 42
