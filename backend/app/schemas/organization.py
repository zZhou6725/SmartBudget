"""组织权限 Schema（与前端 types/organization.ts 对齐）"""
from pydantic import BaseModel, Field


class DeptCreate(BaseModel):
    name: str = Field(..., description="部门名称")
    manager: str = Field("", description="负责人")


class DeptUpdate(BaseModel):
    name: str | None = None
    manager: str | None = None


class DeptResponse(BaseModel):
    id: int
    name: str
    manager: str = ""
    member_count: int = 0
    total_budget: float = 0.0


class UserCreate(BaseModel):
    username: str = Field(..., description="用户名")
    real_name: str = Field("", description="真实姓名")
    dept_id: int | None = None
    role: str = Field("viewer", description="角色")


class UserUpdate(BaseModel):
    real_name: str | None = None
    dept_id: int | None = None
    role: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    real_name: str = ""
    dept_name: str = ""
    role: str = "viewer"
    status: str = "active"