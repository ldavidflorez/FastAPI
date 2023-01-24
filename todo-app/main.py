from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from auth import get_current_user, get_user_exception

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")


def sucessfull_response(status_code: int):
    return {"status": status_code, "transaction": "sucessfull"}


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(
        gt=0, lt=6, description="The priority must be between 1-5")
    complete: bool


@app.get("/")
async def read_todos(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@app.get("/todos/user")
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int,  user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos).filter(
        models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo_model:
        return todo_model
    raise http_exception()


@app.post("/")
async def create_todo(todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()

    return sucessfull_response(201)


@app.put("/todo/{todo_id}")
async def update_todo(todo_id: int, todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos).filter(
        models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo_model:
        todo_model.title = todo.title
        todo_model.description = todo.description
        todo_model.priority = todo.priority
        todo_model.complete = todo.complete

        db.add(todo_model)
        db.commit()

        return sucessfull_response(200)

    raise http_exception()


@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos).filter(
        models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo_model:
        db.query(models.Todos).filter(models.Todos.id == todo_id).filter(
            models.Todos.owner_id == user.get("id")).delete()

        db.commit()

        return sucessfull_response(200)

    raise http_exception()
