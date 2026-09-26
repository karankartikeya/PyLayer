import json

import anyio

from pylayer.logging import log_path
from pylayer.server import server


def test_tools_registered():
    tools = anyio.run(server.list_tools)
    assert {t.name for t in tools} == {"get_signature", "typecheck", "run_sandboxed"}


def test_call_is_logged(pydantic_project, monkeypatch):
    monkeypatch.setenv("PYLAYER_RUN_ID", "test-run")
    anyio.run(server.call_tool, "get_signature",
              {"target": "pydantic.BaseModel.nope_xyz", "project_dir": str(pydantic_project)})
    records = [json.loads(line) for line in log_path().read_text().splitlines()]
    assert records[-1]["tool"] == "get_signature"
    assert records[-1]["status"] == "not_found"
    assert records[-1]["run_id"] == "test-run"
