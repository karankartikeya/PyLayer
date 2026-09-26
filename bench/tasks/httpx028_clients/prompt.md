Create `clients.py` with two httpx helpers:

- `make_client(base_url: str, proxy_url: str | None = None, timeout: float = 5.0) -> httpx.Client`: a client for our API that sends all traffic through `proxy_url` when one is given.
- `async fetch_json(app, path: str) -> dict`: calls an ASGI application (e.g. a Starlette app) in-process with httpx, without starting a server, and returns the decoded JSON of a GET to `path`.
