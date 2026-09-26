Create `config.py` with an `AppConfig` settings class that reads its values from environment variables with the prefix `APP_`:

- `database_url: str` (required)
- `debug: bool = False`
- `workers: int = 4`

Add `load_config() -> AppConfig` that reads the current environment. Missing required values or values of the wrong type should raise a pydantic `ValidationError`.

Please don't add new dependencies; use what's already in requirements.txt.
