import asyncio
import importlib

import httpx
import pytest
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


@pytest.fixture
def mod():
    return importlib.import_module("clients")


def test_make_client_with_proxy(mod, monkeypatch):
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        monkeypatch.delenv(k, raising=False)
    c = mod.make_client("https://api.example.com", "http://proxy.local:3128", timeout=2.0)
    assert isinstance(c, httpx.Client)
    assert str(c.base_url).startswith("https://api.example.com")
    assert c.timeout.connect == 2.0
    assert c._mounts, "proxy should be configured"
    plain = mod.make_client("https://api.example.com")
    assert not plain._mounts


def test_fetch_json_in_process(mod):
    async def ping(request):
        return JSONResponse({"ok": True, "path": request.url.path})

    app = Starlette(routes=[Route("/ping", ping)])
    assert asyncio.run(mod.fetch_json(app, "/ping")) == {"ok": True, "path": "/ping"}
