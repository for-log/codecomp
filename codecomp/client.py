from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from codecomp.depends import get_db
from codecomp.task.repository import (
    TaskAddDTO,
    TaskDTO,
    TaskTestAddDTO,
    get_tasks as rep_get_tasks,
    get_task as rep_get_task,
    create_task as rep_create_task,
    create_task_test as rep_create_task_test,
)


router = APIRouter(prefix="/client", tags=["client"])
templates = Jinja2Templates(directory="templates")


@router.get("/tasks", response_class=HTMLResponse)
async def read_tasks(
    request: Request,
    page: int,
    size: int,
    db: AsyncSession = Depends(get_db),
):
    tasks = await rep_get_tasks(page * size, size, db)
    return templates.TemplateResponse(
        request=request, name="tasks.html", context={"tasks": tasks}
    )


@router.get("/tasks/{task_id}", response_class=HTMLResponse)
async def read_task(
    request: Request,
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    task = await rep_get_task(task_id, db)
    return templates.TemplateResponse(
        request=request, name="task.html", context={"task": task}
    )