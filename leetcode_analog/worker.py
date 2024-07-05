from faststream import FastStream
from faststream.rabbit import RabbitBroker
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import create_subprocess_exec, wait_for
from asyncio.subprocess import PIPE
import psutil
from typing import Generator, Any

from leetcode_analog.enviroment_generators import python_generate
from leetcode_analog.helper import generate_filename


class Incoming(BaseModel):
    user_id: int
    random_id: str
    task_id: int
    lang: str
    inputs: list
    outputs: list
    time_limit: int
    memory_limit: int


# STOP_CAUSE:
#     success
#     timeout
#     error
#     partial
#     memory
class Outgoing(Incoming):
    all: int
    success: int
    stop_cause: str


router = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = FastStream(router)
engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost/leetcode", echo=True
)
session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def process_memory(pid):
    process = psutil.Process(pid)
    mem_info = process.memory_info()
    return mem_info.rss


async def create_and_wait_process(space_limit: int, time_limit: int, *args):
    proc = await create_subprocess_exec(*args, stdout=PIPE, stderr=PIPE)

    if process_memory(proc.pid) / 1024 > space_limit:
        proc.kill()
        return -2

    try:
        await wait_for(proc.wait(), time_limit / 1000)
    except TimeoutError:
        proc.kill()
        return -1
    return proc.returncode


async def process_code(
    func_name,
    message: Incoming,
    filename,
    code_generator: Generator[str, Any, None],
    *args,
):
    for i, arg in enumerate(
        code_generator(func_name, zip(message.inputs, message.outputs), filename)
    ):
        result = await create_and_wait_process(
            message.memory_limit, message.time_limit, *args, arg
        )
        if result == 0:
            continue
        return dict(
            all=len(message.inputs),
            success=i,
            stop_cause=["memory", "timeout", "", "error", "partial"][result + 2],
        )
    return dict(
        all=len(message.inputs), success=len(message.inputs), stop_cause="success"
    )


LANGUAGE_MAP = {"py": (python_generate, "python", "-c")}


@router.subscriber("code-test-queue")
@router.publisher("test-result-queue")
async def execute_tests(m: Incoming) -> Outgoing:
    upload_filename = generate_filename(m.random_id, m.task_id, m.user_id, m.lang)
    args = LANGUAGE_MAP[m.lang]
    result = await process_code(f"task{m.task_id}", m, upload_filename, *args)
    return Outgoing(**m.model_dump(), **result)
