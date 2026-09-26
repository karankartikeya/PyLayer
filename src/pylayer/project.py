"""Resolve the user's project directory and its Python interpreter."""

import os
from pathlib import Path


def resolve_project_dir(project_dir: str | None) -> Path:
    if project_dir:
        return Path(project_dir).expanduser().resolve()
    env = os.environ.get("PYLAYER_PROJECT_DIR")
    return Path(env).expanduser().resolve() if env else Path.cwd().resolve()


def resolve_python(project_dir: Path) -> Path:
    """Project .venv wins; PYLAYER_PYTHON is the fallback. Never the server's own interpreter."""
    venv_python = project_dir / ".venv" / "bin" / "python"
    if venv_python.exists():
        return venv_python
    env = os.environ.get("PYLAYER_PYTHON")
    if env and Path(env).exists():
        return Path(env)
    raise FileNotFoundError(
        f"No project interpreter: {venv_python} does not exist and PYLAYER_PYTHON is not set"
    )
