"""工作台 API 路由（GET /api/v1/workbench/*）"""
from fastapi import APIRouter

from app.core.response import ApiResponse, PageResult
from app.schemas.workbench import WorkbenchOverview, PendingApprovalItem, TrendPoint
from app.schemas.common import PageParams

router = APIRouter(prefix="/workbench", tags=["工作台"])


@router.get("/overview", response_model=ApiResponse[WorkbenchOverview])
async def get_overview():
    """获取概览统计数据"""
    # TODO: service 层实现真实统计逻辑
    return ApiResponse(
        data=WorkbenchOverview(
            total_budget=None,
            total_expense=None,
            remaining_balance=None,
            pending_approvals=None,
            over_budget_depts=None,
        )
    )


@router.get("/pending-approvals", response_model=ApiResponse[PageResult[PendingApprovalItem]])
async def get_pending_approvals(page: int = 1, page_size: int = 10):
    """获取待审批分页列表"""
    # TODO: service 层实现真实查询
    return ApiResponse(
        data=PageResult(
            items=[],
            total=0,
            page=page,
            page_size=page_size,
        )
    )


@router.get("/expense-trend", response_model=ApiResponse[list[TrendPoint]])
async def get_expense_trend():
    """获取支出趋势数据"""
    # TODO: service 层实现真实趋势查询
    return ApiResponse(data=[])