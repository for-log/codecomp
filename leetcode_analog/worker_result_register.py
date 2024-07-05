from fastapi import Depends
from faststream.rabbit.fastapi import RabbitRouter
from sqlalchemy.ext.asyncio import AsyncSession
from os import environ

from leetcode_analog.depends import get_db
from leetcode_analog.resolve import TaskResolve
from leetcode_analog.worker import Outgoing as Incoming

# STOP_CAUSE:
#     timeout
#     error
#     memory

router = RabbitRouter(environ.get("RABBIT_URL"))


@router.subscriber("test-result-queue")
async def register_tests(m: Incoming, db: AsyncSession = Depends(get_db)):
    db.add(
        TaskResolve(
            random_id=m.random_id,
            language=m.lang,
            tests_count=m.all,
            passed_count=m.success,
            stop_cause=m.stop_cause,
            user_id=m.user_id,
            task_id=m.task_id,
        )
    )
    await db.commit()
