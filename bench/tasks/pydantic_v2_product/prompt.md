Create `catalog.py` with a pydantic model `Product`:

- `sku: str` must look like `ABC-1234` (three uppercase letters, a dash, four digits)
- `tags: list[str]` must have between 1 and 5 items
- `price: Decimal` must be greater than 0

When serialized to JSON, `price` must be a string (e.g. `"19.90"`), not a number.

Add `parse_product(data: dict) -> Product` and `product_json(p: Product) -> str`. CI treats DeprecationWarnings as errors.
