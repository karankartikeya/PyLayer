"""Benchmark runner: each task x arm x repeat, run Claude Code headless, score with hidden tests.

Arm A: baseline, no MCP servers.  Arm B: PyLayer MCP server + workspace CLAUDE.md.

Usage:
    uv run python bench/run.py --tasks pydantic_v2_signup,numpy2_signal --arms A,B
    uv run python bench/run.py --limit 3 --repeats 2
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from pylayer.logging import log_path
from pylayer.sandbox import run_test_dir

BENCH = Path(__file__).resolve().parent
REPO = BENCH.parent
TASKS_DIR = BENCH / "tasks"
RESULTS = BENCH / "results" / "results.jsonl"
ARTIFACTS = BENCH / "results" / "artifacts"
PYLAYER_BIN = REPO / ".venv" / "bin" / "pylayer"

CLAUDE_TIMEOUT_S = 900
# Same base tools in both arms: file edits and running python in the workspace venv.
BASE_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash(python *)", "Bash(python3 *)"]
PYLAYER_TOOLS = ["mcp__pylayer__get_signature", "mcp__pylayer__typecheck", "mcp__pylayer__run_sandboxed"]
# Files we put in the workspace; anything else at the end was written by Claude.
SETUP_FILES = {"prompt.md", "requirements.txt", "CLAUDE.md"}
IGNORED_DIRS = {".venv", "hidden_tests", "__pycache__", ".pytest_cache", ".claude"}


def list_tasks() -> list[str]:
    return sorted(p.name for p in TASKS_DIR.iterdir() if (p / "prompt.md").exists())


def clean_env() -> dict[str, str]:
    """Drop Claude Code session vars so a nested `claude -p` doesn't inherit the parent session."""
    return {k: v for k, v in os.environ.items() if not k.startswith("CLAUDE") and k != "VIRTUAL_ENV"}


def make_workspace(task_id: str, label: str, with_venv: bool = True) -> Path:
    task = TASKS_DIR / task_id
    ws = Path(tempfile.mkdtemp(prefix=f"pylayer-{label}-"))
    shutil.copy(task / "requirements.txt", ws / "requirements.txt")
    if with_venv:
        env = clean_env()
        subprocess.run(["uv", "venv", "-q", "--python", "3.12", str(ws / ".venv")], check=True, env=env)
        if (ws / "requirements.txt").read_text().strip():
            subprocess.run(
                ["uv", "pip", "install", "-q", "--python", str(ws / ".venv" / "bin" / "python"),
                 "-r", str(ws / "requirements.txt")],
                check=True, env=env,
            )
    return ws


def score(ws: Path, task_id: str) -> dict:
    """Copy hidden tests in and run only them in the sandbox."""
    dest = ws / "hidden_tests"
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(TASKS_DIR / task_id / "hidden_tests", dest)
    r = run_test_dir(str(ws), "hidden_tests", timeout_s=180)
    return {
        "pass": r.get("exit_code") == 0,
        "test_exit_code": r.get("exit_code"),
        "test_error": r.get("error"),
        "test_output": (r.get("stdout", "") + r.get("stderr", ""))[-3000:],
    }


def claude_files(ws: Path) -> dict[str, str]:
    files = {}
    for p in sorted(ws.rglob("*")):
        rel = p.relative_to(ws)
        if not p.is_file() or rel.parts[0] in IGNORED_DIRS or any(part in IGNORED_DIRS for part in rel.parts):
            continue
        if str(rel) in SETUP_FILES:
            continue
        try:
            files[str(rel)] = p.read_text()
        except UnicodeDecodeError:
            files[str(rel)] = "<binary>"
    return files


def tool_counts(run_id: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    path = log_path()
    if not path.exists():
        return counts
    for line in path.read_text().splitlines():
        rec = json.loads(line)
        if rec.get("run_id") == run_id:
            counts[rec["tool"]] = counts.get(rec["tool"], 0) + 1
    return counts


def claude_cmd(prompt: str, arm: str, run_id: str, ws: Path, model: str | None) -> list[str]:
    cmd = ["claude", "-p", prompt, "--output-format", "json",
           "--setting-sources", "project", "--permission-mode", "dontAsk",
           "--no-session-persistence", "--strict-mcp-config"]
    tools = list(BASE_TOOLS)
    if arm == "B":
        mcp = {"mcpServers": {"pylayer": {
            "type": "stdio", "command": str(PYLAYER_BIN), "args": [],
            "env": {"PYLAYER_RUN_ID": run_id, "PYLAYER_PROJECT_DIR": str(ws)},
        }}}
        tools += PYLAYER_TOOLS
    else:
        mcp = {"mcpServers": {}}
    cmd += ["--mcp-config", json.dumps(mcp), "--allowedTools", *tools]
    if model:
        cmd += ["--model", model]
    return cmd


def run_one(task_id: str, arm: str, repeat: int, model: str | None, keep: bool) -> dict:
    run_id = f"{task_id}.{arm}.{repeat}.{int(time.time())}"
    ws = make_workspace(task_id, f"{task_id}-{arm}")
    task = TASKS_DIR / task_id
    prompt = (task / "prompt.md").read_text()
    shutil.copy(task / "prompt.md", ws / "prompt.md")
    if arm == "B":
        shutil.copy(BENCH / "workspace_CLAUDE.md", ws / "CLAUDE.md")

    env = clean_env()
    env["PATH"] = f"{ws / '.venv' / 'bin'}{os.pathsep}{env.get('PATH', '')}"
    env["VIRTUAL_ENV"] = str(ws / ".venv")

    start = time.monotonic()
    claude_out: dict = {}
    error = None
    try:
        proc = subprocess.run(
            claude_cmd(prompt, arm, run_id, ws, model),
            cwd=ws, env=env, stdin=subprocess.DEVNULL,
            capture_output=True, text=True, timeout=CLAUDE_TIMEOUT_S,
        )
        try:
            claude_out = json.loads(proc.stdout)
        except json.JSONDecodeError:
            error = f"claude exit {proc.returncode}: {(proc.stdout + proc.stderr)[-1000:]}"
    except subprocess.TimeoutExpired:
        error = f"claude timed out after {CLAUDE_TIMEOUT_S}s"
    wall = time.monotonic() - start

    files = claude_files(ws)
    result = score(ws, task_id)

    art = ARTIFACTS / run_id
    art.mkdir(parents=True, exist_ok=True)
    (art / "claude.json").write_text(json.dumps(claude_out, indent=1))
    (art / "test_output.txt").write_text(result["test_output"])
    for rel, content in files.items():
        (art / "files" / rel).parent.mkdir(parents=True, exist_ok=True)
        (art / "files" / rel).write_text(content)

    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "task_id": task_id,
        "arm": arm,
        "repeat": repeat,
        "run_id": run_id,
        "pass": result["pass"],
        "test_exit_code": result["test_exit_code"],
        "test_error": result["test_error"],
        "error": error,
        "is_error": claude_out.get("is_error"),
        "subtype": claude_out.get("subtype"),
        "num_turns": claude_out.get("num_turns"),
        "duration_ms": claude_out.get("duration_ms"),
        "total_cost_usd": claude_out.get("total_cost_usd"),
        "usage": claude_out.get("usage"),
        "models": sorted((claude_out.get("modelUsage") or {}).keys()),
        "wall_s": round(wall, 1),
        "tool_calls": tool_counts(run_id),
        "files": sorted(files),
        "artifact_dir": str(art.relative_to(REPO)),
    }
    if keep:
        record["workspace"] = str(ws)
    else:
        shutil.rmtree(ws, ignore_errors=True)
    return record


def done_keys() -> set[tuple[str, str, int]]:
    if not RESULTS.exists():
        return set()
    keys = set()
    for line in RESULTS.read_text().splitlines():
        r = json.loads(line)
        keys.add((r["task_id"], r["arm"], r["repeat"]))
    return keys


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", help="comma-separated task ids (default: all)")
    ap.add_argument("--arms", default="A,B")
    ap.add_argument("--limit", type=int, help="max number of runs to execute this invocation")
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--model", help="passed to claude --model")
    ap.add_argument("--keep", action="store_true", help="keep workspaces for inspection")
    args = ap.parse_args()

    if not PYLAYER_BIN.exists():
        sys.exit(f"missing {PYLAYER_BIN}; run `uv sync` first")
    tasks = args.tasks.split(",") if args.tasks else list_tasks()
    unknown = set(tasks) - set(list_tasks())
    if unknown:
        sys.exit(f"unknown tasks: {sorted(unknown)}")
    arms = args.arms.split(",")

    done = done_keys()
    todo = [(t, a, r) for r in range(args.repeats) for t in tasks for a in arms if (t, a, r) not in done]
    if args.limit is not None:
        todo = todo[: args.limit]
    print(f"{len(todo)} runs to do ({len(done)} already recorded)")

    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    for i, (task_id, arm, repeat) in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] {task_id} arm={arm} repeat={repeat} ...", flush=True)
        rec = run_one(task_id, arm, repeat, args.model, args.keep)
        with RESULTS.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        tools = ", ".join(f"{k}={v}" for k, v in rec["tool_calls"].items()) or "-"
        print(f"    pass={rec['pass']} turns={rec['num_turns']} wall={rec['wall_s']}s tools: {tools}"
              + (f" error={rec['error'][:120]}" if rec["error"] else ""), flush=True)


if __name__ == "__main__":
    main()
