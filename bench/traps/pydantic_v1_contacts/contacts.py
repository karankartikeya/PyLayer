from pydantic import BaseModel, Field, field_validator


class Contact(BaseModel):
    name: str
    email: str
    tags: list[str] = Field(default_factory=list)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("invalid email")
        return v.lower()

    @field_validator("tags")
    @classmethod
    def dedupe_tags(cls, v: list[str]) -> list[str]:
        return list(dict.fromkeys(v))


def load_contacts(rows: list[dict]) -> list[Contact]:
    return [Contact.model_validate(r) for r in rows]


def export_contacts(contacts: list[Contact]) -> list[dict]:
    return [c.model_dump() for c in contacts]


def contact_schema() -> dict:
    return Contact.model_json_schema()
