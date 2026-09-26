from . import repo
from .schemas import UserCreate, UserOut


class EmailTaken(Exception):
    pass


def register(session, payload: dict) -> dict:
    data = UserCreate.model_validate(payload)
    if repo.find_by_email(session, data.email):
        raise EmailTaken(data.email)
    user = repo.add_user(session, **data.model_dump())
    return UserOut.model_validate(user).model_dump()


def profile(session, user_id: int):
    user = repo.get_user(session, user_id)
    return UserOut.model_validate(user).model_dump() if user else None


def stats(session, user_id: int) -> dict:
    return {"published": repo.count_published(session, user_id)}
