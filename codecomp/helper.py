from jose import jwt
from pydantic import BaseModel
import bcrypt


class Token(BaseModel):
    user_name: str
    user_id: int
    timestamp: int


def hash_password(password: str):
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt).decode("utf-8")


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def generate_token(params: Token) -> str:
    return jwt.encode(params.model_dump(), "secret", algorithm="HS256")


def decode_token(token: str) -> Token:
    raw_token = jwt.decode(token, "secret", algorithms=["HS256"])
    return Token(**raw_token)


def generate_filename(random_id: str, task_id: int, user_id: int, lang: str) -> str:
    return f"{random_id}_{task_id}_{user_id}.{lang}"
