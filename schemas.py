from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    rate: int
    impression: str | None = None


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int
    reader_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True
