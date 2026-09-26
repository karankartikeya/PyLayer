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
    try:
        tag = ensure_image(proj)
    except (RuntimeError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        return {"error": f"sandbox unavailable: {e}"}

    name = f"pylayer-run-{uuid.uuid4().hex[:12]}"
    with tempfile.TemporaryDirectory(prefix="pylayer-") as work:
        work_dir = Path(work)
        if mode == "script":
            (work_dir / "main.py").write_text(code)
            cmd = ["python", "/work/main.py"]
        elif code.strip():
            (work_dir / "test_snippet.py").write_text(code)
            cmd = ["pytest", "-q", "-p", "no:cacheprovider", "--rootdir", "/work", "/work/test_snippet.py"]
        else:
            cmd = ["pytest", "-q", "-p", "no:cacheprovider", "/project"]

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
