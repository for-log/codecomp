from fastapi import FastAPI

from leetcode_analog.user.handlers import router as user_router
from leetcode_analog.task.handlers import router as task_router
from leetcode_analog.worker_result_register import router as queue_router
from leetcode_analog.resolve.handlers import router as resolve_router
from leetcode_analog.depends import Base, engine

app = FastAPI(lifespan=queue_router.lifespan_context)
app.include_router(user_router)
app.include_router(task_router)
app.include_router(queue_router)
app.include_router(resolve_router)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/startup")
async def startup():
    await init_models()
