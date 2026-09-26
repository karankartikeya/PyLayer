import importlib

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.filterwarnings("error::DeprecationWarning")


@pytest.fixture
def mod():
    return importlib.import_module("app")


def test_get_item(mod):
    with TestClient(mod.app) as c:
        r = c.get("/items/apple")
        assert r.status_code == 200
        assert r.json() == {"name": "apple", "quantity": 3}
        assert c.get("/items/kiwi").status_code == 404


def test_list_items(mod):
    with TestClient(mod.app) as c:
        assert sorted(c.get("/items").json()) == ["apple", "pear"]
        assert c.get("/items", params={"in_stock": "true"}).json() == ["apple"]


def test_startup_calls_load_inventory(mod, monkeypatch):
    monkeypatch.setattr(mod, "load_inventory", lambda: {"kiwi": 7})
    with TestClient(mod.app) as c:
        assert c.get("/items").json() == ["kiwi"]
        assert c.get("/items/kiwi").json() == {"name": "kiwi", "quantity": 7}
