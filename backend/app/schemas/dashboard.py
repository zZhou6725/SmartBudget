"""数据看板 Schema（与前端 types/dashboard.ts 字段完全对齐）"""
from pydantic import BaseModel


class TrendItem(BaseModel):
    """支出趋势"""
    month: str
    amount: float


class DeptRankItem(BaseModel):
    """部门排名"""
    dept_name: str
    amount: float
    usage_rate: float


class CategoryPieItem(BaseModel):
    """费用类型占比"""
    category: str
    amount: float
    percent: float


class BudgetExecItem(BaseModel):
    """预算执行"""
    dept_name: str
    budget: float
    used: float
    rate: float