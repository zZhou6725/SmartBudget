"""数据看板 API 路由（/api/v1/dashboard）"""
from fastapi import APIRouter, Query

from app.core.response import ApiResponse
from app.schemas.dashboard import TrendItem, DeptRankItem, CategoryPieItem, BudgetExecItem
from app.service import dashboard as dashboard_service

router = APIRouter(prefix="/dashboard", tags=["数据看板"])


@router.get("/trend", response_model=ApiResponse[list[TrendItem]])
async def get_trend(
    month: str | None = Query(None, description="月份筛选"),
    dept_name: str | None = Query(None, description="部门筛选"),
):
    """支出趋势"""
    data = await dashboard_service.get_trend(month, dept_name)
    return ApiResponse(data=data)


@router.get("/dept-rank", response_model=ApiResponse[list[DeptRankItem]])
async def get_dept_rank(month: str | None = Query(None, description="月份筛选")):
    """部门支出排名"""
    data = await dashboard_service.get_dept_rank(month)
    return ApiResponse(data=data)


@router.get("/category-pie", response_model=ApiResponse[list[CategoryPieItem]])
async def get_category_pie(
    month: str | None = Query(None, description="月份筛选"),
    dept_name: str | None = Query(None, description="部门筛选"),
):
    """费用类型占比"""
    data = await dashboard_service.get_category_pie(month, dept_name)
    return ApiResponse(data=data)


@router.get("/budget-exec", response_model=ApiResponse[list[BudgetExecItem]])
async def get_budget_exec(year: int | None = Query(None, description="年份筛选")):
    """预算执行"""
    data = await dashboard_service.get_budget_exec(year)
    return ApiResponse(data=data)