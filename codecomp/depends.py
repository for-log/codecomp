from typing import Annotated
from fastapi import Depends, HTTPException, Header
from jose import JWTError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
from sqlalchemy.orm import declarative_base

from os import environ
from codecomp.helper import decode_token

engine = create_async_engine(
    environ.get("POSTGRES_URL"), echo=True
)
session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
redis_pool = redis.ConnectionPool.from_url(environ.get("REDIS_URL"))
Base = declarative_base()


# from fastapi docs
async def get_db():
    db = session()
    try:
        yield db
    finally:
        await db.close()


async def get_redis():
    conn = redis.Redis(connection_pool=redis_pool)
    try:
        yield conn
    finally:
        await conn.close()


async def auth_middleware(
    Authentication: Annotated[str | None, Header()] = None,
    redis: redis.Redis = Depends(get_redis),
):
    if not Authentication:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        params = decode_token(Authentication)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = await redis.get(f"user_token_{params.user_id}")
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return params
