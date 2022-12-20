from typing import Optional
from fastapi import FastAPI
from enum import Enum

app = FastAPI()


class DirectionName(str, Enum):
    north = "north"
    south = "south"
    east = "east"
    west = "west"


BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
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


@app.get("/directions/{direction_name}")
async def get_durection(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"direction": direction_name}
    elif direction_name == DirectionName.south:
        return {"direction": direction_name}
    elif direction_name == DirectionName.east:
        return {"direction": direction_name}
    else:
        return {"direction": direction_name}
