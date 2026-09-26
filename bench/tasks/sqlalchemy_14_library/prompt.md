Create `library.py` using the SQLAlchemy ORM:

- a declarative base named `Base`
- `Author` (`id`, `name` unique) and `Book` (`id`, `title`, `year`, `author_id` foreign key), with relationships `Author.books` and `Book.author`

Functions:
- `init_db(engine)` creates the tables
- `add_book(session, author_name: str, title: str, year: int) -> Book` adds a book, reusing an existing author with that name if there is one
- `books_by_author(session, author_name: str) -> list[str]` returns that author's book titles sorted by year
