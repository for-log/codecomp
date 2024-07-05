from typing import Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import datetime

from . import Task, TaskTest


class TaskAddDTO(BaseModel):
    title: str
    description: str
    level: int
    time_complexity: Optional[int] = None
    space_complexity: Optional[int] = None


class TaskDTO(TaskAddDTO):
    id: int
    author_id: int
    created_at: datetime.datetime


async def create_task(
    task_dto: TaskAddDTO, author_id: int, db: AsyncSession
) -> TaskDTO:
    task = Task(**task_dto.model_dump(), author_id=author_id)
    db.add(task)
    await db.commit()
    return TaskDTO.model_validate(task, from_attributes=True)


async def get_tasks(offset: int, count: int, db: AsyncSession) -> list[TaskDTO]:
    tasks_orm = await db.scalars(select(Task).offset(offset).limit(count))
    return [TaskDTO.model_validate(task, from_attributes=True) for task in tasks_orm]


async def get_task(task_id: int, db: AsyncSession) -> Optional[TaskDTO]:
    task_orm = await db.scalar(select(Task).where(Task.id == task_id))
    if not task_orm:
        return None
    return TaskDTO.model_validate(task_orm, from_attributes=True)


class TaskTestAddDTO(BaseModel):
    input: str
    output: str
    task_id: int


class TaskTestDTO(TaskTestAddDTO):
    id: int


async def get_task_tests(task_id: int, db: AsyncSession) -> list[TaskTestDTO]:
    task_test_orm = await db.scalars(
        select(TaskTest).where(TaskTest.task_id == task_id)
    )
    return [
        TaskTestDTO.model_validate(test, from_attributes=True) for test in task_test_orm
    ]

# Not DTO because we don't want to send tests to the client
async def get_task_with_tests(task_id: int, db: AsyncSession) -> Optional[Task]:
    task_orm = await db.scalar(
        select(Task)
        .options(selectinload(Task.tests))
        .where(Task.id == task_id)
    )
    if not task_orm:
        return None
    return task_orm


async def create_task_test(
    task_test_dto: TaskTestAddDTO, db: AsyncSession
) -> TaskTestDTO:
    """
    input and output are must be valid json strings
    """
    task_test = TaskTest(**task_test_dto.model_dump())
    db.add(task_test)
    await db.commit()
    return TaskTestDTO.model_validate(task_test, from_attributes=True)
