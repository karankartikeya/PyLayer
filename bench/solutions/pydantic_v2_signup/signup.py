from pydantic import BaseModel, field_validator, model_validator


class SignupForm(BaseModel):
    username: str
    password: str
    password_confirm: str
    referral_code: str | None = None

    @field_validator("username")
    @classmethod
    def normalize_username(cls, v: str) -> str:
        return v.strip().lower()

    @model_validator(mode="after")
    def passwords_match(self) -> "SignupForm":
        if self.password != self.password_confirm:
            raise ValueError("passwords do not match")
        return self


def to_payload(form: SignupForm) -> dict:
    return form.model_dump(exclude={"password_confirm"}, exclude_none=True)
