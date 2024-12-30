from typing import List
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy import String
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author", cascade="all, delete", lazy="select")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, created_at={self.created_at!r}, updated_at={self.updated_at!r})"


class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(unique=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user_account.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    author: Mapped["User"] = relationship("User", back_populates="posts", cascade="all, delete")
    category: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, post_id={self.post_id!r}, author_id={self.author_id!r}, category={self.category!r}, content={self.content!r}, created_at={self.created_at!r})"
