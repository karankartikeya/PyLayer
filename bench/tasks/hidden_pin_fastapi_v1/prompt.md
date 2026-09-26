Create `api.py` with a FastAPI app named `app`, using pydantic models for the request and response bodies.

- `POST /users` accepts JSON `{"email": str, "age": int, "nickname": str (optional)}`. Normalize the email to lowercase and reject ages under 13 with a 422. Store the user in memory with a generated integer `id` (starting at 1) and return it. Leave `nickname` out of responses when it wasn't provided.
- `GET /users/{user_id}` returns the stored user, or 404.
