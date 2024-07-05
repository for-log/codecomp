from typing import Optional
from pydantic import BaseModel
from uuid import UUID
import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from codecomp.helper import generate_filename
from . import TaskResolve


class CodeDTO(BaseModel):
    code: str
    lang: str


class ResolveDTO(BaseModel):
    id: int
    random_id: UUID
    language: str
    tests_count: int
    passed_count: int
    stop_cause: str
    user_id: int
    task_id: int
    created_at: datetime.datetime


async def get_task_resolves(
    task_id: int, user_id: int, db: AsyncSession
) -> list[ResolveDTO]:
    resolves_orm = await db.scalars(
        select(TaskResolve).where(
            TaskResolve.task_id == task_id, TaskResolve.user_id == user_id
        )
    )
    return [
        ResolveDTO.model_validate(resolve, from_attributes=True)
        for resolve in resolves_orm
    ]


class ResolveWithCodeDTO(ResolveDTO):
    code: str


async def get_task_resolve_with_code(
    user_id: int, resolve_id: str, db: AsyncSession
) -> Optional[ResolveWithCodeDTO]:
    resolve_orm = await db.scalar(
        select(TaskResolve).where(
            TaskResolve.user_id == user_id,
            TaskResolve.random_id == resolve_id,
        )
    )
    if not resolve_orm:
        return None

    filename = generate_filename(
        resolve_orm.random_id,
        resolve_orm.task_id,
        resolve_orm.user_id,
        resolve_orm.language,
    )
    with open(f"./uploads/{filename}", "r") as f:
        setattr(resolve_orm, "code", f.read())

    resolve = ResolveWithCodeDTO.model_validate(resolve_orm, from_attributes=True)
    return resolve
