Create `contacts.py` with a pydantic model `Contact` with fields `name: str`, `email: str` and `tags: list[str]` (default empty list).

- Emails should be normalized to lowercase and must contain an `@`; reject them otherwise.
- Tags should be deduplicated, preserving their original order.

Also add:
- `load_contacts(rows: list[dict]) -> list[Contact]`
- `export_contacts(contacts: list[Contact]) -> list[dict]` returning plain dicts
- `contact_schema() -> dict` returning the JSON schema of `Contact`
