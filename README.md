# PyLayer

Local MCP server (stdio) that grounds Claude Code in a project's real Python environment.

Tools:

- `get_signature(target, project_dir)`: introspects a dotted path using the project's `.venv/bin/python` (fallback `PYLAYER_PYTHON`). Returns signature, docstring head, package version, members, a deprecation flag, or `exists: false` with "did you mean" suggestions.
- `typecheck(code | path, project_dir)`: basedpyright (standard mode) against the project interpreter; ≤30 diagnostics.
- `run_sandboxed(code, project_dir, mode, timeout_s)`: Docker, `--network none --memory 512m --cpus 1 --pids-limit 128`, project mounted read-only at `/project`. Image `pylayer-env:<hash>` built once per `requirements.txt`.

Every call is appended to `logs/tool_calls.jsonl` (override dir with `PYLAYER_LOG_DIR`; tag runs with `PYLAYER_RUN_ID`).

```sh
uv sync
uv run pytest          # sandbox tests skip if Docker isn't running
uv run pylayer         # start the stdio server
```

## Benchmark

```sh
uv run python bench/verify_tasks.py              # reference solutions pass, traps fail
uv run python bench/run.py --tasks a,b --arms A,B  # resumable; appends to bench/results/results.jsonl
uv run python bench/report.py                    # markdown summary
```

Arm A: Claude Code with file tools and `python` only. Arm B: same plus the PyLayer MCP server and `bench/workspace_CLAUDE.md`.
Runs use `--setting-sources project` and `--strict-mcp-config` so user-level hooks, plugins and MCP servers don't leak in.
