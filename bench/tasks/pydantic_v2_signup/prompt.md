Create `signup.py` with a pydantic model `SignupForm` with fields `username: str`, `password: str`, `password_confirm: str` and an optional `referral_code: str | None = None`.

- `username` should be stripped of surrounding whitespace and lowercased.
- The form must be rejected if `password` and `password_confirm` don't match.

Also add `to_payload(form: SignupForm) -> dict` that returns the form's data without `password_confirm` and without any fields whose value is None.

Our CI runs with DeprecationWarnings treated as errors.
