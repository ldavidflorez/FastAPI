from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
import uuid
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Book description",
                                       min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": str(uuid.uuid4()),
                "title": "A title",
                "author": "An author",
                "description": "An awesome description about book...",
                "rating": 75
            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Book description",
                                       min_length=1, max_length=100)


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_exception_handler(request: Request, exception: NegativeNumberException):
    return JSONResponse(status_code=418, content={"message": f"You want {exception.books_to_return} books. "
                        f"You only must put positive values"})


@app.post("/books/login")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username, "password": password}


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}


@app.get("/assigment/login")
async def login(book_id: UUID, username: str = Header(), password: str = Header()):
    if (username and password) and (username == "FastAPIUser" and password == "test1234!"):
        for b in BOOKS:
            if b.id == book_id:
                return b
        raise raise_book_not_found_exception(book_id)
    return "Invalid User"


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return)
    if len(BOOKS) < 1:
        create_books_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        return BOOKS[:books_to_return]
    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for b in BOOKS:
        if b.id == book_id:
            return b
    raise raise_book_not_found_exception(book_id)


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_not_rating(book_id: UUID):
    for b in BOOKS:
        if b.id == book_id:
            return b
    raise raise_book_not_found_exception(book_id)


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    for i, b in enumerate(BOOKS):
        if b.id == book_id:
            BOOKS[i] = book
            return BOOKS[i]
    raise raise_book_not_found_exception(book_id)


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    for i, b in enumerate(BOOKS):
        if b.id == book_id:
            del BOOKS[i]
            return f"id {book_id} was deleted"
    raise raise_book_not_found_exception(book_id)


def create_books_no_api():
    book_1 = Book(id=str(uuid.uuid4()),
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60)
    book_2 = Book(id=str(uuid.uuid4()),
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=70)
    book_3 = Book(id=str(uuid.uuid4()),
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=80)
    book_4 = Book(id=str(uuid.uuid4()),
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=90)
    book_5 = Book(id=str(uuid.uuid4()),
                  title="Title 5",
                  author="Author 5",
                  description="Description 5",
                  rating=100)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
    BOOKS.append(book_5)


def raise_book_not_found_exception(book_id):
    return HTTPException(status_code=404, detail=f"Book {book_id} not found",
                         headers={"X-Header-Error": "Nothing to be seen at the UUID"})
