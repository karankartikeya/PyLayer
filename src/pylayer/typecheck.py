"""typecheck: run basedpyright against the project's interpreter."""

import json
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

from pylayer.project import resolve_project_dir, resolve_python

MAX_DIAGNOSTICS = 30
TIMEOUT_S = 120


def _basedpyright() -> str:
    local = Path(sys.executable).parent / "basedpyright"
    return str(local) if local.exists() else (shutil.which("basedpyright") or "basedpyright")


def typecheck(code: str | None = None, path: str | None = None, project_dir: str | None = None) -> dict:
    if (code is None) == (path is None):
        return {"error": "pass exactly one of `code` or `path`"}

    proj = resolve_project_dir(project_dir)
    try:
        python = resolve_python(proj)
    except FileNotFoundError as e:
        return {"error": str(e)}

    tmp_file: Path | None = None
    if code is not None:
        # Inside the project so local imports resolve.
        tmp_file = proj / f"_pylayer_check_{uuid.uuid4().hex[:8]}.py"
        tmp_file.write_text(code)
        target = tmp_file
    else:
        target = Path(path).expanduser()
        if not target.is_absolute():
            target = proj / target
        if not target.exists():
            return {"error": f"file not found: {target}"}

    # "standard" mode: real errors, not basedpyright's strict-by-default noise.
    # Config lives outside the project so we never touch the user's files.
    with tempfile.TemporaryDirectory() as cfg_dir:
        cfg = Path(cfg_dir) / "pyrightconfig.json"
        cfg.write_text(json.dumps({"typeCheckingMode": "standard", "extraPaths": [str(proj)]}))
        try:
            proc = subprocess.run(
                [_basedpyright(), "--outputjson", "--pythonpath", str(python), "-p", str(cfg), str(target)],
                cwd=proj,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_S,
            )
        except subprocess.TimeoutExpired:
            return {"error": f"type checker timed out after {TIMEOUT_S}s"}
        finally:
            if tmp_file is not None:
                tmp_file.unlink(missing_ok=True)

    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"error": f"type checker failed (exit {proc.returncode}): {(proc.stdout + proc.stderr)[-1500:]}"}

    diagnostics = []
    for d in report.get("generalDiagnostics", []):
        if d.get("severity") not in ("error", "warning"):
            continue
        diagnostics.append({
            "file": "<code>" if tmp_file is not None else d.get("file"),
            "line": d.get("range", {}).get("start", {}).get("line", -1) + 1,
            "severity": d["severity"],
            "message": d.get("message", ""),
            "rule": d.get("rule"),
        })

    errors = sum(1 for d in diagnostics if d["severity"] == "error")
    warnings = len(diagnostics) - errors
    return {
        "summary": f"{errors} errors, {warnings} warnings",
        "errors": errors,
        "warnings": warnings,
        "diagnostics": diagnostics[:MAX_DIAGNOSTICS],
        "truncated": len(diagnostics) > MAX_DIAGNOSTICS,
    }
