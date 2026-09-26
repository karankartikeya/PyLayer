# PyLayer checks

This project has a PyLayer MCP server. Before using any third-party library API you are not certain about for the installed version, call `get_signature`. Before finishing, call `typecheck` on every file you changed, then `run_sandboxed` to execute it. If either reports errors, fix them and check again. Do not finish while checks fail.
