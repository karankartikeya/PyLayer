from typing import List

from pydantic import BaseModel, validator


class Contact(BaseModel):
    name: str
    email: str
    tags: List[str] = []

    @validator("email")
    def normalize_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("invalid email")
        return v.lower()

    @validator("tags")
    def dedupe_tags(cls, v: List[str]) -> List[str]:
        return list(dict.fromkeys(v))


def load_contacts(rows: list[dict]) -> list[Contact]:
    return [Contact.parse_obj(r) for r in rows]


def export_contacts(contacts: list[Contact]) -> list[dict]:
    return [c.dict() for c in contacts]


def contact_schema() -> dict:
    return Contact.schema()
