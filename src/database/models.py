from datetime import datetime

from sqlalchemy import (Boolean, DateTime, String, Text, func)
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column)


class Base(DeclarativeBase):
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    notify_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_reminded: Mapped[bool] = mapped_column(Boolean, default=False)
    is_happened: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[int]


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(220), nullable=True)
    username: Mapped[str] = mapped_column(String(110), nullable=True)
    # is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
