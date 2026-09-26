from pylayer.typecheck import typecheck

GOOD = """\
from pydantic import BaseModel

class User(BaseModel):
    name: str

u = User.model_validate({"name": "a"})
print(u.model_dump())
"""

BAD = """\
from pydantic import BaseModel

class User(BaseModel):
    name: str

u = User.parse_obj_v3({"name": "a"})
x: int = "not an int"
"""


def test_clean_code(pydantic_project):
    r = typecheck(code=GOOD, project_dir=str(pydantic_project))
    assert r["errors"] == 0, r
    assert r["summary"].startswith("0 errors")


def test_catches_errors_against_installed_pydantic(pydantic_project):
    r = typecheck(code=BAD, project_dir=str(pydantic_project))
    assert r["errors"] >= 2, r
    messages = " ".join(d["message"] for d in r["diagnostics"])
    assert "parse_obj_v3" in messages
    lines = {d["line"] for d in r["diagnostics"]}
    assert {6, 7} <= lines


def test_path_mode_and_no_temp_leftovers(pydantic_project):
    f = pydantic_project / "mod.py"
    f.write_text("y: str = 1\n")
    r = typecheck(path="mod.py", project_dir=str(pydantic_project))
    assert r["errors"] == 1
    assert not list(pydantic_project.glob("_pylayer_check_*.py"))


def test_requires_one_input(pydantic_project):
    assert "error" in typecheck(project_dir=str(pydantic_project))
