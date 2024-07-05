from jose import JWTError
from pydantic import BaseModel
from sqlalchemy import select
from leetcode_analog.helper import check_password, hash_password, generate_token, Token
from leetcode_analog.error import ErrorResult, ErrorCode
from leetcode_analog.user import User
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from time import time


class UserAddDTO(BaseModel):
    name: str
    email: str
    password: str


async def create_user(
    register_dto: UserAddDTO, db: AsyncSession, redis: redis
) -> dict:
    hashed_password = hash_password(register_dto.password)
    user = User(**register_dto.model_dump(), password=hashed_password)
    try:
        db.add(user)
        await db.commit()
        token_struct = generate_token(
            Token(user_id=user.id, user_name=user.name, timestamp=int(time()))
        )
        await redis.set(f"user_token_{user.id}", token_struct)
        return {"token": token_struct}
    except JWTError:
        return ErrorResult(error_code=ErrorCode.WTF)
    except Exception:
        return ErrorResult(error_code=ErrorCode.USER_EXISTS)


class UserDTO(BaseModel):
    email: str
    password: str


async def login_user(user_dto: UserDTO, db: AsyncSession, redis: redis) -> dict:
    user = await db.scalar(select(User).where(User.email == user_dto.email))
    if not user:
        return ErrorResult(error_code=ErrorCode.USER_NOT_FOUND)
    if not check_password(user_dto.password, user.password):
        return ErrorResult(error_code=ErrorCode.WRONG_PASSWORD)
    try:
        token_struct = generate_token(
            Token(user_id=user.id, user_name=user.name, timestamp=int(time()))
        )
        await redis.set(f"user_token_{user.id}", token_struct)
        return {"token": token_struct}
    except JWTError:
        return ErrorResult(error_code=ErrorCode.WTF)