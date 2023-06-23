from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    books = relationship("Book", back_populates="reader")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    rate = Column(Integer, index=True)
    impression = Column(String, index=True)
    reader_id = Column(Integer, ForeignKey("users.id"))

    reader = relationship("User", back_populates="books")
