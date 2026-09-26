from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

app = FastAPI()
_users: Dict[int, dict] = {}


class UserIn(BaseModel):
    email: str
    age: int
    nickname: Optional[str] = None

    @validator("email")
    def lower_email(cls, v):
        return v.lower()

    @validator("age")
    def check_age(cls, v):
        if v < 13:
            raise ValueError("must be at least 13")
        return v


class UserOut(UserIn):
    id: int


@app.post("/users", response_model=UserOut, response_model_exclude_none=True)
def create_user(user: UserIn):
    uid = len(_users) + 1
    _users[uid] = {"id": uid, **user.dict()}
    return _users[uid]


@app.get("/users/{user_id}", response_model=UserOut, response_model_exclude_none=True)
def get_user(user_id: int):
    if user_id not in _users:
        raise HTTPException(status_code=404, detail="user not found")
    return _users[user_id]
