from pylayer.sandbox import _tail, image_tag, run_sandboxed

from conftest import requires_docker


def test_tail_truncation():
    assert _tail("abc") == "abc"
    out = _tail("x" * 5000 + "END")
    assert out.endswith("END")
    assert "truncated" in out


def test_image_tag_depends_on_requirements():
    assert image_tag("pydantic==2.11.7") != image_tag("pydantic==2.10.0")
    assert image_tag("a") == image_tag("a")


@requires_docker
def test_runs_script_with_project_deps(pydantic_project):
    r = run_sandboxed("import pydantic; print(pydantic.VERSION)", str(pydantic_project))
    assert r["exit_code"] == 0, r
    assert "2.11.7" in r["stdout"]


@requires_docker
def test_network_blocked(pydantic_project):
    code = "import socket; socket.create_connection(('1.1.1.1', 80), timeout=3); print('CONNECTED')"
    r = run_sandboxed(code, str(pydantic_project))
    assert r["exit_code"] != 0
    assert "CONNECTED" not in r["stdout"]


@requires_docker
def test_timeout_enforced(pydantic_project):
    r = run_sandboxed("import time; time.sleep(60)", str(pydantic_project), timeout_s=5)
    assert r["timed_out"] is True
    assert r["duration_s"] < 20


@requires_docker
def test_project_is_read_only(pydantic_project):
    r = run_sandboxed("open('/project/pwned.txt', 'w').write('x')", str(pydantic_project))
    assert r["exit_code"] != 0
    assert "Read-only file system" in r["stderr"]
    assert not (pydantic_project / "pwned.txt").exists()


@requires_docker
def test_pytest_mode(pydantic_project):
    tests = "def test_ok():\n    assert 1 + 1 == 2\n\ndef test_bad():\n    assert False\n"
    r = run_sandboxed(tests, str(pydantic_project), mode="pytest")
    assert r["exit_code"] == 1
    assert "1 failed, 1 passed" in r["stdout"]
