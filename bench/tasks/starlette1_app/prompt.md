Create `app.py`: a plain Starlette application named `app` (no FastAPI).

- Define `open_store() -> dict` returning `{"hits": 0}` and `close_store(store: dict) -> None` which sets `store["closed"] = True`.
- When the app starts up, create the store with `open_store()`; when it shuts down, call `close_store(store)`.
- `GET /hit` increments `hits` and returns JSON `{"hits": n}`.
- `GET /boom` raises a `KeyError`.
- Register an exception handler that turns any `KeyError` into a 404 JSON response `{"error": "not found"}`.
