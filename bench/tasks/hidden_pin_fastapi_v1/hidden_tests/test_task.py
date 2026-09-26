import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    mod = importlib.import_module("api")
    return TestClient(mod.app)


def test_create_and_get(client):
    r = client.post("/users", json={"email": "Ann@X.IO", "age": 30})
    assert r.status_code in (200, 201), r.text
    body = r.json()
    assert body["email"] == "ann@x.io" and body["age"] == 30
    assert "nickname" not in body
    uid = body["id"]
    assert isinstance(uid, int)
    assert client.get(f"/users/{uid}").json()["email"] == "ann@x.io"


def test_nickname_kept(client):
    r = client.post("/users", json={"email": "b@x.io", "age": 20, "nickname": "bee"})
    assert r.json()["nickname"] == "bee"


def test_underage_rejected(client):
    assert client.post("/users", json={"email": "c@x.io", "age": 12}).status_code == 422


def test_missing_user(client):
    assert client.get("/users/9999").status_code == 404
