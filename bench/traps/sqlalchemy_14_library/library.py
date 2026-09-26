from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    year: Mapped[int]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped[Author] = relationship(back_populates="books")


def init_db(engine):
    Base.metadata.create_all(engine)


def add_book(session, author_name: str, title: str, year: int) -> Book:
    author = session.scalars(select(Author).where(Author.name == author_name)).one_or_none()
    if author is None:
        author = Author(name=author_name)
        session.add(author)
    book = Book(title=title, year=year, author=author)
    session.add(book)
    session.flush()
    return book


def books_by_author(session, author_name: str) -> list[str]:
    stmt = select(Book.title).join(Book.author).where(Author.name == author_name).order_by(Book.year)
    return list(session.scalars(stmt))
