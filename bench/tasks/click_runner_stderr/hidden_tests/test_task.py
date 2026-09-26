import importlib

import pytest


@pytest.fixture
def mod():
    return importlib.import_module("tool")


def test_counts_lines(mod, tmp_path):
    p = tmp_path / "f.txt"
    p.write_text("a\nb\nc\n")
    out, err, code = mod.run_cli([str(p)])
    assert (out.strip(), err.strip(), code) == ("3", "", 0)


def test_missing_file(mod, tmp_path):
    missing = str(tmp_path / "nope.txt")
    out, err, code = mod.run_cli([missing])
    assert code == 1
    assert out.strip() == ""
    assert err.strip() == f"error: no such file: {missing}"
