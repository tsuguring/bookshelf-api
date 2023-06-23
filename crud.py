from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_book(db: Session, user_id: int, book_id: int):
    return (
        db.query(models.Book)
        .filter(models.Book.id == book_id, models.Book.reader_id == user_id)
        .first()
    )


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate, user_id: int):
    db_book = models.Book(**book.dict(), reader_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book: schemas.Book):
    db.delete(book)
    db.commit()
    return book


def update_book(db: Session, book: schemas.BookUpdate, req_book: schemas.BookUpdate):
    for field, value in req_book.dict(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book
