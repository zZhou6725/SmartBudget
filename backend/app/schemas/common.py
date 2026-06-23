"""通用 Schema（分页参数）"""
from pydantic import BaseModel


class PageParams(BaseModel):
    """分页请求参数（与前端 PageParams 对齐）"""
    page: int = 1
    page_size: int = 10