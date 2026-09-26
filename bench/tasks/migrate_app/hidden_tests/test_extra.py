import pytest

from app import db, service

pytestmark = pytest.mark.filterwarnings("error::DeprecationWarning")


@pytest.fixture
def session(tmp_path):
    s = db.make_session(db.make_engine(f"sqlite:///{tmp_path / 'x.db'}"))
    yield s
    s.close()


def test_nickname_optional_like_before(session):
    out = service.register(session, {"email": "n@x.io", "name": "N"})
    assert out["nickname"] is None


def test_missing_profile(session):
    assert service.profile(session, 12345) is None


def test_profile_is_plain_dicts(session):
    uid = service.register(session, {"email": "p@x.io", "name": "P", "nickname": None})["id"]
    prof = service.profile(session, uid)
    assert type(prof) is dict and type(prof["posts"]) is list
