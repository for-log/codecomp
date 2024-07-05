import datetime
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from uuid import UUID

from codecomp.depends import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    experience: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    created_tasks: Mapped[List["Task"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
    resolves: Mapped[List["TaskResolve"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )