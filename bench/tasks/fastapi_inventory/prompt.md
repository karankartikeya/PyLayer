Create `app.py` with a FastAPI application named `app`.

- Define `load_inventory() -> dict[str, int]` returning `{"apple": 3, "pear": 0}`. When the application starts up, load the inventory into memory by calling `load_inventory()`; clear it on shutdown.
- `GET /items/{name}` returns `{"name": ..., "quantity": ...}` using a pydantic response model, or 404 if the item is unknown.
- `GET /items` returns the list of item names; with `?in_stock=true` only items with quantity > 0.

CI treats DeprecationWarnings as errors.
