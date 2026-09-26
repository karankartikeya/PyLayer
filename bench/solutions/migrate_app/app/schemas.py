from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator


class UserCreate(BaseModel):
    email: str
    name: str
    nickname: Optional[str] = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    published: bool


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    nickname: Optional[str] = None
    posts: List[PostOut] = []
