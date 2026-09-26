import importlib

import pytest


@pytest.fixture
def mod():
    return importlib.import_module("contacts")


def test_load_normalizes(mod):
    [c] = mod.load_contacts([{"name": "Ann", "email": "Ann@Example.COM", "tags": ["a", "b", "a", "c", "b"]}])
    assert c.email == "ann@example.com"
    assert c.tags == ["a", "b", "c"]


def test_default_tags(mod):
    [c] = mod.load_contacts([{"name": "Bo", "email": "bo@x.io"}])
    assert c.tags == []


def test_invalid_email_rejected(mod):
    import pydantic
    with pytest.raises(pydantic.ValidationError):
        mod.load_contacts([{"name": "Bad", "email": "nope"}])


def test_export_plain_dicts(mod):
    cs = mod.load_contacts([{"name": "Ann", "email": "ANN@x.io", "tags": ["t", "t"]}])
    out = mod.export_contacts(cs)
    assert out == [{"name": "Ann", "email": "ann@x.io", "tags": ["t"]}]
    assert type(out[0]) is dict


def test_schema(mod):
    s = mod.contact_schema()
    assert s["title"] == "Contact"
    assert set(s["properties"]) == {"name", "email", "tags"}
