import importlib

import pytest


@pytest.fixture
def mod():
    return importlib.import_module("config")


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    for k in ("APP_DATABASE_URL", "APP_DEBUG", "APP_WORKERS"):
        monkeypatch.delenv(k, raising=False)


def test_reads_env(mod, monkeypatch):
    monkeypatch.setenv("APP_DATABASE_URL", "sqlite:///x.db")
    monkeypatch.setenv("APP_DEBUG", "true")
    monkeypatch.setenv("APP_WORKERS", "8")
    c = mod.load_config()
    assert isinstance(c, mod.AppConfig)
    assert (c.database_url, c.debug, c.workers) == ("sqlite:///x.db", True, 8)


def test_defaults(mod, monkeypatch):
    monkeypatch.setenv("APP_DATABASE_URL", "postgres://h/db")
    c = mod.load_config()
    assert (c.debug, c.workers) == (False, 4)


def test_missing_required(mod):
    import pydantic
    with pytest.raises(pydantic.ValidationError):
        mod.load_config()


def test_bad_type(mod, monkeypatch):
    import pydantic
    monkeypatch.setenv("APP_DATABASE_URL", "x")
    monkeypatch.setenv("APP_WORKERS", "many")
    with pytest.raises(pydantic.ValidationError):
        mod.load_config()


def test_unprefixed_ignored(mod, monkeypatch):
    monkeypatch.setenv("APP_DATABASE_URL", "x")
    monkeypatch.setenv("WORKERS", "99")
    assert mod.load_config().workers == 4
