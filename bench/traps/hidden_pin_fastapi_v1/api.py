from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI()
_users: dict[int, dict] = {}


class UserIn(BaseModel):
    email: str
    age: int
    nickname: str | None = None

    @field_validator("email")
    @classmethod
    def lower_email(cls, v: str) -> str:
        return v.lower()

    @field_validator("age")
    @classmethod
    def check_age(cls, v: int) -> int:
        if v < 13:
            raise ValueError("must be at least 13")
        return v


class UserOut(UserIn):
    id: int


@app.post("/users", response_model=UserOut, response_model_exclude_none=True)
def create_user(user: UserIn):
    uid = len(_users) + 1
    _users[uid] = {"id": uid, **user.model_dump()}
    return _users[uid]


@app.get("/users/{user_id}", response_model=UserOut, response_model_exclude_none=True)
def get_user(user_id: int):
    if user_id not in _users:
        raise HTTPException(status_code=404, detail="user not found")
    return _users[user_id]
