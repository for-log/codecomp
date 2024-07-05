import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from codecomp.depends import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    level: Mapped[int]
    time_complexity: Mapped[Optional[int]] = mapped_column(default=None)
    space_complexity: Mapped[Optional[int]] = mapped_column(default=None)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    author: Mapped["User"] = relationship(back_populates="created_tasks")
    resolves: Mapped[List["TaskResolve"]] = relationship(
        back_populates="task", cascade="all, delete-orphan"
    )
    tests: Mapped[List["TaskTest"]] = relationship(
        back_populates="task", cascade="all, delete-orphan"
    )


class TaskTest(Base):
    __tablename__ = "task_test"

    id: Mapped[int] = mapped_column(primary_key=True)
    input: Mapped[str]
    output: Mapped[str]
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))

    task: Mapped["Task"] = relationship(back_populates="tests")
