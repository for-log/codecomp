from fastapi import APIRouter, Depends
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession

from codecomp.depends import get_db, get_redis
from codecomp.error import ErrorResult
from codecomp.user.repository import UserAddDTO, UserDTO, create_user, login_user as rep_login_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def register_user(
    register_dto: UserAddDTO,
    db: AsyncSession = Depends(get_db),
    redis: redis.Redis = Depends(get_redis),
) -> dict[str, str] | ErrorResult:
    return await create_user(register_dto, db, redis)


@router.post("/login")
async def login_user(
    login_dto: UserDTO,
    db: AsyncSession = Depends(get_db),
    redis: redis.Redis = Depends(get_redis),
) -> dict[str, str] | ErrorResult:
    return await rep_login_user(login_dto, db, redis)
