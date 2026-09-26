from pydantic import BaseModel, root_validator, validator


class SignupForm(BaseModel):
    username: str
    password: str
    password_confirm: str
    referral_code: str | None = None

    @validator("username")
    def normalize_username(cls, v):
        return v.strip().lower()

    @root_validator(skip_on_failure=True)
    def passwords_match(cls, values):
        if values.get("password") != values.get("password_confirm"):
            raise ValueError("passwords do not match")
        return values


def to_payload(form: SignupForm) -> dict:
    return form.dict(exclude={"password_confirm"}, exclude_none=True)
