"""预算管理 业务逻辑层（当前返回空占位数据）"""
from app.schemas.budget import (
    BudgetCreate, BudgetUpdate, BudgetAdjust,
    BudgetResponse, BudgetSummary,
)


async def get_budget_list(
    keyword: str | None = None,
    dept_name: str | None = None,
    year: int | None = None,
    page: int = 1,
    page_size: int = 10,
) -> tuple[list[BudgetResponse], int]:
    """分页查询预算列表"""
    return [], 0


async def get_budget_summary() -> BudgetSummary:
    """预算统计摘要"""
    return BudgetSummary()


async def get_budget_detail(budget_id: int) -> BudgetResponse | None:
    """预算详情"""
    return None


async def create_budget(data: BudgetCreate) -> BudgetResponse:
    """新增预算"""
    return BudgetResponse(id=0, **data.model_dump(), used_amount=0, remaining=data.total_amount)


async def update_budget(budget_id: int, data: BudgetUpdate) -> BudgetResponse | None:
    """编辑预算"""
    return None


async def adjust_budget(budget_id: int, data: BudgetAdjust) -> BudgetResponse | None:
    """预算调整（追加/削减）"""
    return None


async def delete_budget(budget_id: int) -> bool:
    """删除预算"""
    return True