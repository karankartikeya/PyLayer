from . import repo
from .schemas import UserCreate, UserOut


class EmailTaken(Exception):
    pass


def register(session, payload: dict) -> dict:
    data = UserCreate.parse_obj(payload)
    if repo.find_by_email(session, data.email):
        raise EmailTaken(data.email)
    user = repo.add_user(session, **data.dict())
    return UserOut.from_orm(user).dict()


def profile(session, user_id: int):
    user = repo.get_user(session, user_id)
    return UserOut.from_orm(user).dict() if user else None


def stats(session, user_id: int) -> dict:
    return {"published": repo.count_published(session, user_id)}
