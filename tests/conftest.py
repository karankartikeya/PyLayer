import os
import shutil
import subprocess
from pathlib import Path

import pytest

PYDANTIC_PIN = "pydantic==2.11.7"
CLICK_PIN = "click==8.5.0"


@pytest.fixture(autouse=True)
def isolated_log(tmp_path, monkeypatch):
    monkeypatch.setenv("PYLAYER_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.delenv("PYLAYER_PYTHON", raising=False)


@pytest.fixture(scope="session")
def pydantic_project(tmp_path_factory) -> Path:
    """A project dir with its own .venv containing pydantic v2 (not the server's env)."""
    proj = tmp_path_factory.mktemp("pydantic_proj")
    (proj / "requirements.txt").write_text(f"{PYDANTIC_PIN}\n{CLICK_PIN}\n")
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    subprocess.run(["uv", "venv", "--python", "3.12", str(proj / ".venv")], check=True, capture_output=True, env=env)
    subprocess.run(
        ["uv", "pip", "install", "--python", str(proj / ".venv" / "bin" / "python"), PYDANTIC_PIN, CLICK_PIN],
        check=True, capture_output=True, env=env,
    )
    return proj


def docker_available() -> bool:
    if not shutil.which("docker"):
        return False
    return subprocess.run(["docker", "info"], capture_output=True).returncode == 0


requires_docker = pytest.mark.skipif(not docker_available(), reason="Docker daemon not running")
