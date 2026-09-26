Create `tool.py` with:

- a click command `main` that takes a `PATH` argument and prints the number of lines in that file to stdout. If the file doesn't exist it prints `error: no such file: PATH` to stderr and exits with code 1.
- `run_cli(args: list[str]) -> tuple[str, str, int]`: runs `main` in-process with click's testing runner and returns `(stdout, stderr, exit_code)`, with stdout and stderr captured separately.
