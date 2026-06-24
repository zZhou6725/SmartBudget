"""个人中心 Schema（与前端 types/profile.ts 对齐）"""
from pydantic import BaseModel, Field


class ProfileUpdate(BaseModel):
    real_name: str | None = None
    email: str | None = None
    phone: str | None = None


class PasswordChange(BaseModel):
    old_password: str = Field(..., description="原密码")
    new_password: str = Field(..., min_length=6, description="新密码(≥6位)")


class UserProfileResponse(BaseModel):
    id: int
    username: str
    real_name: str = ""
    email: str = ""
    phone: str = ""
    dept_name: str = ""
    role: str = ""
    avatar: str = ""