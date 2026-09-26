"""Append-only JSONL log of every tool call."""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]


def log_path() -> Path:
    log_dir = Path(os.environ.get("PYLAYER_LOG_DIR", REPO_ROOT / "logs"))
    return log_dir / "tool_calls.jsonl"


def log_call(tool: str, args: dict[str, Any], status: str, duration_s: float, **extra: Any) -> None:
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "run_id": os.environ.get("PYLAYER_RUN_ID"),
        "tool": tool,
        "args": args,
        "status": status,
        "duration_s": round(duration_s, 3),
        **extra,
    }
    path = log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(record) + "\n")


class Timer:
    def __enter__(self) -> "Timer":
        self.start = time.monotonic()
        return self

    def __exit__(self, *exc: object) -> None:
        self.elapsed = time.monotonic() - self.start
