from pydantic import BaseModel
from enum import Enum

class ErrorCode(int, Enum):
    USER_NOT_FOUND = 1
    USER_EXISTS = 2
    WRONG_PASSWORD = 3
    WTF = 1000

class ErrorResult(BaseModel):
    error_code: int