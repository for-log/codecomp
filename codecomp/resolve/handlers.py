from json import loads
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from codecomp.worker_result_register import router as queue_router
from codecomp.worker import Incoming as Input
from . import repository as resolve_repository
from codecomp.task import repository as task_repository
from codecomp.depends import auth_middleware, get_db
from codecomp.helper import Token, generate_filename
from uuid import uuid4

router = APIRouter(prefix="/resolves", tags=["resolves"])


@router.get("/{resolve_id}")
async def get_resolve(
    resolve_id: str,
    token: Token = Depends(auth_middleware),
    db: AsyncSession = Depends(get_db),
):
    return await resolve_repository.get_task_resolve_with_code(
        token.user_id, resolve_id, db
    )


@router.get("/")
async def get_resolves(
    task_id: int,
    token: Token = Depends(auth_middleware),
    db: AsyncSession = Depends(get_db),
):
    return await resolve_repository.get_task_resolves(task_id, token.user_id, db)


@router.post("/{task_id}")
async def create_resolve(
    task_id: int,
    dto: resolve_repository.CodeDTO,
    token: Token = Depends(auth_middleware),
    db: AsyncSession = Depends(get_db),
) -> str:
    random_id = str(uuid4())
    upload_filename = generate_filename(random_id, task_id, token.user_id, dto.lang)
    with open(f"./uploads/{upload_filename}", "w") as buffer:
        buffer.write(dto.code)

    task = await task_repository.get_task_with_tests(task_id, db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    inputs = [loads(task_test.input) for task_test in task.tests]
    outputs = [loads(task_test.output) for task_test in task.tests]

    input = Input(
        user_id=token.user_id,
        task_id=task_id,
        lang=dto.lang,
        random_id=random_id,
        inputs=inputs,
        outputs=outputs,
        time_limit=task.time_complexity,
        memory_limit=task.space_complexity,
    )

    await queue_router.broker.publish(
        input,
        "code-test-queue",
    )

    return random_id
