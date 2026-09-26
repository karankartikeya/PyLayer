from sqlalchemy import func, select, text

from .models import Post, User


def add_user(session, email, name, nickname=None):
    user = User(email=email, name=name, nickname=nickname)
    session.add(user)
    session.commit()
    return user


def add_post(session, user_id, title, published=False):
    post = Post(user_id=user_id, title=title, published=published)
    session.add(post)
    session.commit()
    return post


def get_user(session, user_id):
    return session.get(User, user_id)


def find_by_email(session, email):
    return session.execute(select(User).where(User.email == email)).scalars().first()


def count_published(session, user_id):
    stmt = select(func.count(Post.id)).where(Post.user_id == user_id, Post.published.is_(True))
    return session.execute(stmt).scalar_one()


def user_emails(engine):
    with engine.connect() as conn:
        return [row.email for row in conn.execute(text("select email from users order by email"))]
