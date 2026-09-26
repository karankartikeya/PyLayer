import pytest

from app import db, repo, service


@pytest.fixture
def engine(tmp_path):
    return db.make_engine(f"sqlite:///{tmp_path / 'app.db'}")


@pytest.fixture
def session(engine):
    s = db.make_session(engine)
    yield s
    s.close()


def test_register_and_profile(session):
    out = service.register(session, {"email": " Ann@X.io ", "name": "Ann", "nickname": "a"})
    assert out["email"] == "ann@x.io"
    prof = service.profile(session, out["id"])
    assert prof["name"] == "Ann" and prof["posts"] == []


def test_duplicate_email(session):
    service.register(session, {"email": "a@x.io", "name": "A", "nickname": None})
    with pytest.raises(service.EmailTaken):
        service.register(session, {"email": "A@x.io", "name": "A2", "nickname": None})


def test_posts_and_stats(session):
    uid = service.register(session, {"email": "b@x.io", "name": "B", "nickname": None})["id"]
    repo.add_post(session, uid, "one", published=True)
    repo.add_post(session, uid, "two")
    prof = service.profile(session, uid)
    assert [p["title"] for p in prof["posts"]] == ["one", "two"]
    assert service.stats(session, uid) == {"published": 1}


def test_user_emails(engine, session):
    service.register(session, {"email": "z@x.io", "name": "Z", "nickname": None})
    service.register(session, {"email": "m@x.io", "name": "M", "nickname": None})
    assert repo.user_emails(engine) == ["m@x.io", "z@x.io"]
