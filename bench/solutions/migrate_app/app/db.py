from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


def make_engine(url: str):
    return create_engine(url)


def make_session(engine):
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
