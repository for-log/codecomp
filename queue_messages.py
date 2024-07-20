from pydantic import BaseModel


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