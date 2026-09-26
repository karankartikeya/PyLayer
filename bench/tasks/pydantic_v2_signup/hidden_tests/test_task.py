import importlib

import pytest

pytestmark = pytest.mark.filterwarnings("error::DeprecationWarning")


@pytest.fixture
def mod():
    return importlib.import_module("signup")


def test_username_normalized(mod):
    f = mod.SignupForm(username="  Alice ", password="pw", password_confirm="pw")
    assert f.username == "alice"


def test_password_mismatch_rejected(mod):
    import pydantic
    with pytest.raises(pydantic.ValidationError):
        mod.SignupForm(username="bob", password="a", password_confirm="b")


def test_payload_excludes_confirm_and_none(mod):
    f = mod.SignupForm(username="Bob", password="pw", password_confirm="pw")
    assert mod.to_payload(f) == {"username": "bob", "password": "pw"}
    f2 = mod.SignupForm(username="Bob", password="pw", password_confirm="pw", referral_code="X1")
    assert mod.to_payload(f2) == {"username": "bob", "password": "pw", "referral_code": "X1"}
