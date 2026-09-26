import sys

from pylayer.introspect import get_signature


def test_real_signature(pydantic_project):
    r = get_signature("pydantic.BaseModel.model_validate", str(pydantic_project))
    assert r["exists"] is True
    assert r["kind"] == "function"
    assert "obj" in r["signature"]
    assert r["package"] == "pydantic"
    assert r["version"] == "2.11.7"
    assert r["interpreter"].startswith(str(pydantic_project))


def test_missing_attribute_suggests(pydantic_project):
    r = get_signature("pydantic.BaseModel.parse_obj_v3", str(pydantic_project))
    assert r["exists"] is False
    assert r["nearest_parent"] == "pydantic.BaseModel"
    assert 0 < len(r["suggestions"]) <= 5
    assert "pydantic.BaseModel.parse_obj (deprecated)" in r["suggestions"]


def test_deprecated_target_flagged(pydantic_project):
    r = get_signature("pydantic.BaseModel.parse_obj", str(pydantic_project))
    assert r["exists"] is True
    assert "model_validate" in r["deprecated"]
    assert "deprecated" not in get_signature("pydantic.BaseModel.model_validate", str(pydantic_project))


def test_class_lists_members(pydantic_project):
    r = get_signature("pydantic.BaseModel", str(pydantic_project))
    assert r["kind"] == "class"
    assert "model_dump" in r["members"]
    assert all(not m.startswith("_") for m in r["members"])


def test_module_and_missing_module(pydantic_project):
    assert get_signature("pydantic", str(pydantic_project))["kind"] == "module"
    r = get_signature("not_a_real_pkg_xyz.thing", str(pydantic_project))
    assert r["exists"] is False
    assert "error" in r


def test_uses_project_interpreter_not_server(pydantic_project, tmp_path):
    # pydantic is also in the server env (via mcp); a project without it must not see it.
    bare = tmp_path / "bare"
    bare.mkdir()
    (bare / ".venv" / "bin").mkdir(parents=True)
    (bare / ".venv" / "bin" / "python").symlink_to(sys.base_prefix + "/bin/python3.12")
    r = get_signature("pydantic.BaseModel", str(bare))
    assert r["exists"] is False


def test_no_interpreter(tmp_path):
    r = get_signature("json.dumps", str(tmp_path))
    assert r["exists"] is False
    assert "No project interpreter" in r["error"]


def test_env_fallback(tmp_path, monkeypatch):
    monkeypatch.setenv("PYLAYER_PYTHON", sys.base_prefix + "/bin/python3.12")
    r = get_signature("json.dumps", str(tmp_path))
    assert r["exists"] is True
    assert r["kind"] == "function"


def test_getattr_deprecation_warning_reported(pydantic_project):
    # click 8.2+ hides MultiCommand from dir() and serves it via a warning module __getattr__.
    r = get_signature("click.MultiCommand", str(pydantic_project))
    assert r["exists"] is True
    assert any("MultiCommand" in w and "deprecated" in w for w in r["warnings"])
    assert "warnings" not in get_signature("click.Group", str(pydantic_project))
