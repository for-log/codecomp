import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from uuid import UUID

from leetcode_analog.depends import Base


class TaskResolve(Base):
    __tablename__ = "task_resolve"

    id: Mapped[int] = mapped_column(primary_key=True)
    random_id: Mapped[UUID] = mapped_column(unique=True)
    language: Mapped[str]
    tests_count: Mapped[int]
    passed_count: Mapped[int]
    stop_cause: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="resolves")
    task: Mapped["Task"] = relationship(back_populates="resolves")