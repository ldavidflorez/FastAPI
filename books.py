from typing import Optional
from fastapi import FastAPI

app = FastAPI()

BOOKS = {
    "book_1": {"title": "Title One", "author": "Author One"},
    "book_2": {"title": "Title Two", "author": "Author Two"},
    "book_3": {"title": "Title Three", "author": "Author Three"},
    "book_4": {"title": "Title Four", "author": "Author Four"},
    "book_5": {"title": "Title Five", "author": "Author Five"},
}


@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS


@app.get("/books/{book_name}")
async def read_one_book(book_name: str):
    return BOOKS[book_name]


@app.get("/assigment/")
async def read_one_book(book_name: str):
    return BOOKS[book_name]


@app.post("/")
async def create_book(book_title: str, book_author: str):
    last_book_id = max([int(book.split("_")[-1]) for book in BOOKS])
    BOOKS[f"book_{last_book_id + 1}"] = {"title": book_title,
                                         "author": book_author}
    return BOOKS[f"book_{last_book_id + 1}"]


@app.put("/{book_name}")
async def update_book(book_name: str, book_title: Optional[str] = None, book_author: Optional[str] = None):
    if book_title:
        BOOKS[book_name]["title"] = book_title
    if book_author:
        BOOKS[book_name]["author"] = book_author
    return BOOKS[book_name]


@app.delete("/{book_name}")
async def delete_book(book_name: str):
    del BOOKS[book_name]
    return {"message": f"{book_name} was deleted"}


@app.delete("/assigment/")
async def delete_book(book_name: str):
    del BOOKS[book_name]
    return {"message": f"{book_name} was deleted"}
