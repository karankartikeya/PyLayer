import importlib

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


@pytest.fixture
def mod():
    return importlib.import_module("library")


@pytest.fixture
def session(mod, tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'lib.db'}")
    mod.init_db(engine)
    with Session(engine) as s:
        yield s


def test_add_and_query(mod, session):
    mod.add_book(session, "Le Guin", "The Dispossessed", 1974)
    mod.add_book(session, "Le Guin", "A Wizard of Earthsea", 1968)
    mod.add_book(session, "Banks", "Excession", 1996)
    session.commit()
    assert mod.books_by_author(session, "Le Guin") == ["A Wizard of Earthsea", "The Dispossessed"]
    assert mod.books_by_author(session, "Banks") == ["Excession"]
    assert mod.books_by_author(session, "Nobody") == []


def test_author_reused(mod, session):
    b1 = mod.add_book(session, "Le Guin", "One", 1970)
    b2 = mod.add_book(session, "Le Guin", "Two", 1971)
    session.commit()
    assert b1.author.id == b2.author.id
    assert session.query(mod.Author).count() == 1
    assert sorted(b.title for b in b1.author.books) == ["One", "Two"]
