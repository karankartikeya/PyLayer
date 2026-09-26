import importlib

import pytest
from sqlalchemy import create_engine, text


@pytest.fixture
def mod():
    return importlib.import_module("report")


@pytest.fixture
def engine(tmp_path):
    eng = create_engine(f"sqlite:///{tmp_path / 'r.db'}")
    with eng.begin() as c:
        c.execute(text("create table users (id integer primary key, name text, age integer)"))
        c.execute(text("create table orders (id integer primary key, user_id integer)"))
        c.execute(text("insert into users (name, age) values ('ann', 31), ('bo', 19), ('cy', 45)"))
        c.execute(text("insert into orders (user_id) values (1), (1)"))
    return eng


def test_run_query_with_params(mod, engine):
    rows = mod.run_query(engine, "select name, age from users where age > :min_age order by age", {"min_age": 20})
    assert rows == [{"name": "ann", "age": 31}, {"name": "cy", "age": 45}]
    assert all(type(r) is dict for r in rows)


def test_run_query_no_params(mod, engine):
    assert mod.run_query(engine, "select count(*) as n from users") == [{"n": 3}]


def test_table_counts(mod, engine):
    assert mod.table_counts(engine, ["users", "orders"]) == {"users": 3, "orders": 2}
