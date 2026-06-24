"""数据看板 业务逻辑层（当前返回空占位数据）"""
from app.schemas.dashboard import TrendItem, DeptRankItem, CategoryPieItem, BudgetExecItem


async def get_trend(month: str | None = None, dept_name: str | None = None) -> list[TrendItem]:
    """支出趋势 — 后续聚合查询"""
    return []


async def get_dept_rank(month: str | None = None) -> list[DeptRankItem]:
    """部门排名 — 后续聚合查询"""
    return []


async def get_category_pie(month: str | None = None, dept_name: str | None = None) -> list[CategoryPieItem]:
    """费用类型占比 — 后续聚合查询"""
    return []


async def get_budget_exec(year: int | None = None) -> list[BudgetExecItem]:
    """预算执行 — 后续聚合查询"""
    return []