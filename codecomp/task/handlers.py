from json import loads
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from codecomp.depends import auth_middleware, get_db
from codecomp.helper import Token
from codecomp.task.repository import (
    TaskAddDTO,
    TaskDTO,
    TaskTestAddDTO,
    get_tasks as rep_get_tasks,
    get_task as rep_get_task,
    create_task as rep_create_task,
    create_task_test as rep_create_task_test,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
async def get_tasks(db: AsyncSession = Depends(get_db)) -> list[TaskDTO]:
    return await rep_get_tasks(0, 100, db)


@router.get("/{task_id}")
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)) -> TaskDTO:
    return await rep_get_task(task_id, db)


@router.post("/")
async def create_task(
    task_dto: TaskAddDTO,
    token: Token = Depends(auth_middleware),
    db: AsyncSession = Depends(get_db),
) -> TaskDTO:
    return await rep_create_task(task_dto, token.user_id, db)


@router.post("/test")
async def create_test(
    test_dto: TaskTestAddDTO,
    token: Token = Depends(auth_middleware),
    db: AsyncSession = Depends(get_db),
):
    try:
        loads(test_dto.input)
        loads(test_dto.output)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    task = await rep_get_task(test_dto.task_id, db)
    if not task or task.author_id != token.user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return await rep_create_task_test(test_dto, db)
