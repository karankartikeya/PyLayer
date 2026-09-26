Create `schemas.py` with a marshmallow `EventSchema`:

- `title`: required string
- `tags`: list of strings; when missing from the input, loading should give an empty list
- `status`: string; when dumping an object that has no `status`, output `"draft"`
- `starts_at`: datetime

Add `load_events(payload: list[dict]) -> list[dict]` that loads a list of events in one schema call and returns them sorted by `starts_at`. Do the sorting inside the schema, in a post-load hook that receives the whole collection. Unknown input keys should be ignored.

Also add `dump_event(obj) -> dict`.
