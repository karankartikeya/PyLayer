"""run_sandboxed: execute code in a network-less Docker container."""

import hashlib
import subprocess
import tempfile
import time
import uuid
from pathlib import Path
from typing import Literal

from pylayer.project import resolve_project_dir

BASE_IMAGE = "python:3.12-slim"
BUILD_TIMEOUT_S = 900
MAX_OUTPUT = 4000

DOCKERFILE = f"""\
FROM {BASE_IMAGE}
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt pytest
"""


def _tail(text: str) -> str:
    if len(text) <= MAX_OUTPUT:
        return text
    return f"...[truncated {len(text) - MAX_OUTPUT} chars]\n" + text[-MAX_OUTPUT:]


def image_tag(requirements: str) -> str:
    digest = hashlib.sha256((DOCKERFILE + requirements).encode()).hexdigest()[:16]
    return f"pylayer-env:{digest}"


def ensure_image(project_dir: Path) -> str:
    req_file = project_dir / "requirements.txt"
    requirements = req_file.read_text() if req_file.exists() else ""
    tag = image_tag(requirements)

    exists = subprocess.run(["docker", "image", "inspect", tag], capture_output=True)
    if exists.returncode == 0:
        return tag

    with tempfile.TemporaryDirectory() as ctx:
        (Path(ctx) / "Dockerfile").write_text(DOCKERFILE)
        (Path(ctx) / "requirements.txt").write_text(requirements)
        proc = subprocess.run(
            ["docker", "build", "-q", "-t", tag, ctx],
            capture_output=True, text=True, timeout=BUILD_TIMEOUT_S,
        )
    if proc.returncode != 0:
        raise RuntimeError(f"image build failed: {_tail(proc.stderr)}")
    return tag


def run_sandboxed(
    code: str,
    project_dir: str | None = None,
    mode: Literal["script", "pytest"] = "script",
    timeout_s: int = 30,
) -> dict:
    proj = resolve_project_dir(project_dir)
    if mode == "script":
        files, cmd = {"main.py": code}, ["python", "/work/main.py"]
    elif code.strip():
        files = {"test_snippet.py": code}
        cmd = ["pytest", "-q", "-p", "no:cacheprovider", "--rootdir", "/work", "/work/test_snippet.py"]
    else:
        files, cmd = {}, ["pytest", "-q", "-p", "no:cacheprovider", "/project"]
    return _run(proj, cmd, files, timeout_s)


def run_test_dir(project_dir: str, rel_path: str, timeout_s: int = 120) -> dict:
    """Run pytest on one directory of the project, isolated from any pytest config/conftest the project has.

    Used by the benchmark scorer, not exposed as an MCP tool.
    """
    proj = resolve_project_dir(project_dir)
    ini = "[pytest]\n"
    target = f"/project/{rel_path}"
    cmd = ["pytest", "-q", "-p", "no:cacheprovider", "-c", "/work/pytest.ini", "--rootdir", target, target]
    return _run(proj, cmd, {"pytest.ini": ini}, timeout_s)


def _run(proj: Path, cmd: list[str], files: dict[str, str], timeout_s: int) -> dict:
    try:
        tag = ensure_image(proj)
    except (RuntimeError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        return {"error": f"sandbox unavailable: {e}"}

    name = f"pylayer-run-{uuid.uuid4().hex[:12]}"
    with tempfile.TemporaryDirectory(prefix="pylayer-") as work:
        work_dir = Path(work)
        for fname, content in files.items():
            (work_dir / fname).write_text(content)

        docker_cmd = [
            "docker", "run", "--rm", "--name", name,
            "--network", "none",
            "--memory", "512m", "--cpus", "1", "--pids-limit", "128",
            "-v", f"{proj}:/project:ro",
            "-v", f"{work_dir}:/work",
            "-e", "PYTHONPATH=/project",
            "-w", "/project",
            tag, *cmd,
        ]

        start = time.monotonic()
        timed_out = False
        try:
            proc = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=timeout_s)
            exit_code, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired as e:
            # Killing the docker CLI does not stop the container; kill it by name.
            subprocess.run(["docker", "kill", name], capture_output=True)
            timed_out = True
            exit_code = None
            stdout = e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
            stderr = e.stderr.decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        duration = time.monotonic() - start

    return {
        "exit_code": exit_code,
        "stdout": _tail(stdout),
        "stderr": _tail(stderr),
        "timed_out": timed_out,
        "duration_s": round(duration, 2),
        "image": tag,
    }
