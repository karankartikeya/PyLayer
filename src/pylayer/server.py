"""PyLayer MCP server (stdio): get_signature, typecheck, run_sandboxed."""

from typing import Any, Literal

from mcp.server.mcpserver import MCPServer

from pylayer import introspect, sandbox, typecheck as tc
from pylayer.logging import Timer, log_call

server = MCPServer(
    name="pylayer",
    instructions=(
        "Grounds Python work in the project's real installed environment. "
        "Use get_signature before relying on a third-party API, then typecheck and run_sandboxed before finishing."
    ),
)


@server.tool()
def get_signature(target: str, project_dir: str | None = None) -> dict[str, Any]:
    """Look up a dotted path (e.g. `pydantic.BaseModel.model_validate`) in the project's installed packages.

    Returns whether it exists, its kind, signature, docstring head, package version and public members.
    If it does not exist, returns up to 5 close matches ("did you mean").
    """
    with Timer() as t:
        result = introspect.get_signature(target, project_dir)
    status = "error" if "error" in result else ("ok" if result.get("exists") else "not_found")
    log_call("get_signature", {"target": target}, status, t.elapsed)
    return result


@server.tool()
def typecheck(code: str | None = None, path: str | None = None, project_dir: str | None = None) -> dict[str, Any]:
    """Type-check a code string or a file path with basedpyright against the project's interpreter.

    Pass exactly one of `code` or `path`. Returns up to 30 diagnostics and an `N errors, M warnings` summary.
    """
    with Timer() as t:
        result = tc.typecheck(code, path, project_dir)
    status = "error" if "error" in result else "ok"
    log_call("typecheck", {"path": path, "code_chars": len(code) if code else None}, status, t.elapsed,
             errors=result.get("errors"))
    return result


@server.tool()
def run_sandboxed(
    code: str,
    project_dir: str | None = None,
    mode: Literal["script", "pytest"] = "script",
    timeout_s: int = 30,
) -> dict[str, Any]:
    """Run code in a Docker sandbox (no network, 512MB, project mounted read-only at /project).

    mode="script" runs the code as a script. mode="pytest" runs the code as a test file,
    or the project's own tests when `code` is empty.
    """
    with Timer() as t:
        result = sandbox.run_sandboxed(code, project_dir, mode, timeout_s)
    status = "error" if "error" in result else "ok"
    log_call("run_sandboxed", {"mode": mode, "code_chars": len(code)}, status, t.elapsed,
             exit_code=result.get("exit_code"), timed_out=result.get("timed_out"))
    return result


def main() -> None:
    server.run("stdio")


if __name__ == "__main__":
    main()
