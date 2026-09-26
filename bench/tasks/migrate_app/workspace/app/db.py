from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def make_engine(url: str):
    return create_engine(url)


def make_session(engine):
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
