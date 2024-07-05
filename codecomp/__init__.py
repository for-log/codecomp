from fastapi import FastAPI

from codecomp.user.handlers import router as user_router
from codecomp.task.handlers import router as task_router
from codecomp.worker_result_register import router as queue_router
from codecomp.resolve.handlers import router as resolve_router
from codecomp.depends import Base, engine

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
