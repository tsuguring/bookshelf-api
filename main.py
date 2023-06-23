from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello!!"}


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="f{db_user} already registered.",
        )
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.post("/users/{user_id}/books/", response_model=schemas.Book)
def create_book(user_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_book(db=db, book=book, user_id=user_id)


@app.put("/users/{user_id}/books/{book_id}")
def update_book(
    user_id: int, book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)
):
    db_user_book = crud.get_user_book(db, user_id=user_id, book_id=book_id)
    if db_user_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.update_book(db, db_user_book, book)


@app.delete("/users/{user_id}/books/{book_id}")
def delete_book(user_id: int, book_id: int, db: Session = Depends(get_db)):
    db_user_book = crud.get_user_book(db, user_id=user_id, book_id=book_id)
    if db_user_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.delete_book(db, db_user_book)
