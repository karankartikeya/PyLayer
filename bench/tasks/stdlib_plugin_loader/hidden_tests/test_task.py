import importlib

import pytest


@pytest.fixture
def mod():
    return importlib.import_module("plugins")


def test_load_and_reload(mod, tmp_path):
    p = tmp_path / "greeter.py"
    p.write_text("VALUE = 1\n\ndef hello():\n    return 'hi'\n")
    m = mod.load_plugin(str(p))
    assert m.__name__ == "greeter"
    assert m.hello() == "hi" and m.VALUE == 1
    p.write_text("VALUE = 2\n\ndef hello():\n    return 'yo'\n")
    m2 = mod.reload_plugin(m)
    assert m2.VALUE == 2 and m2.hello() == "yo"


def test_two_plugins_independent(mod, tmp_path):
    (tmp_path / "a_plug.py").write_text("NAME = 'a'\n")
    (tmp_path / "b_plug.py").write_text("NAME = 'b'\n")
    a = mod.load_plugin(str(tmp_path / "a_plug.py"))
    b = mod.load_plugin(str(tmp_path / "b_plug.py"))
    assert (a.NAME, b.NAME) == ("a", "b")
