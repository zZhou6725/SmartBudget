"""鉴权 Schema（与前端 types/auth.ts 对齐）"""
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user_info: dict