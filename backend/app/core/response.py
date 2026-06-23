"""统一返回体（与前端 ApiResponse / PageResult 完全对齐）"""
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一 API 返回体"""
    code: int = 0
    data: T | None = None
    msg: str = "success"


class PageResult(BaseModel, Generic[T]):
    """分页查询结果"""
    items: list[T]
    total: int
    page: int
    page_size: int