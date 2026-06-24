"""工作台 API"""
from fastapi import APIRouter, Query
from app.core.response import ApiResponse, PageResult
from app.schemas.workbench import WorkbenchOverview, PendingApprovalItem, TrendPoint
from app.service import workbench as workbench_service

router = APIRouter(prefix="/workbench", tags=["工作台"])


@router.get("/overview", response_model=ApiResponse[WorkbenchOverview])
async def get_overview():
    data = await workbench_service.get_overview()
    return ApiResponse(data=WorkbenchOverview(**data))


@router.get("/pending-approvals", response_model=ApiResponse[PageResult[PendingApprovalItem]])
async def get_pending_approvals(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    items, total = await workbench_service.get_pending_approvals(page, page_size)
    return ApiResponse(data=PageResult(items=items, total=total, page=page, page_size=page_size))


@router.get("/expense-trend", response_model=ApiResponse[list[TrendPoint]])
async def get_expense_trend():
    data = await workbench_service.get_expense_trend()
    return ApiResponse(data=data)