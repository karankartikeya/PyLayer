from sqlalchemy import Column, ForeignKey, Integer, String, select
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("Author", back_populates="books")


def init_db(engine):
    Base.metadata.create_all(engine)


def add_book(session, author_name: str, title: str, year: int) -> Book:
    author = session.execute(select(Author).where(Author.name == author_name)).scalar_one_or_none()
    if author is None:
        author = Author(name=author_name)
        session.add(author)
    book = Book(title=title, year=year, author=author)
    session.add(book)
    session.flush()
    return book


def books_by_author(session, author_name: str) -> list[str]:
    stmt = select(Book.title).join(Book.author).where(Author.name == author_name).order_by(Book.year)
    return list(session.execute(stmt).scalars())
