from __future__ import annotations # Add this at line 1
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True, max_length=255)
    full_name: str = Field(max_length=255)
    name_suffix: str


class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    posts: list["Post"] = Relationship(back_populates="owner")
    address: str = Field(default=None)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class PostBase(SQLModel):
    title: str = Field(max_length=200)
    body: str


class Post(PostBase, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="users.id", nullable=False)
    post_name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    owner: Optional[User] = Relationship(back_populates="posts")
