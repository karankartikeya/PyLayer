from typing import List, Optional

from pydantic import BaseModel, validator


class UserCreate(BaseModel):
    email: str
    name: str
    nickname: Optional[str]

    @validator("email")
    def normalize_email(cls, v):
        return v.strip().lower()


class PostOut(BaseModel):
    id: int
    title: str
    published: bool

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: str
    name: str
    nickname: Optional[str]
    posts: List[PostOut] = []

    class Config:
        orm_mode = True
