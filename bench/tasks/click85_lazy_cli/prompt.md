Create a click CLI where subcommands are loaded lazily.

- `cli.py`: defines `COMMANDS = {"greet": "commands_greet:greet", "sum": "commands_sum:sum_cmd"}` and a command group `cli` implemented with a custom group class that only imports a command's module when that command is looked up (so `import cli` must not import `commands_greet` or `commands_sum`). `cli --help` should list both commands.
- `commands_greet.py`: `greet NAME [--shout]` prints `Hello, NAME!` (all uppercase with `--shout`).
- `commands_sum.py`: `sum N [N ...]` prints the integer sum of the arguments.

CI treats DeprecationWarnings as errors.
