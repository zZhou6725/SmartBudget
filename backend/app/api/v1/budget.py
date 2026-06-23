"""预算管理 API 路由（/api/v1/budgets）"""
from fastapi import APIRouter, Query

from app.core.response import ApiResponse, PageResult
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetAdjust, BudgetResponse, BudgetSummary
from app.service import budget as budget_service

router = APIRouter(prefix="/budgets", tags=["预算管理"])


@router.get("", response_model=ApiResponse[PageResult[BudgetResponse]])
async def list_budgets(
    keyword: str | None = Query(None, description="关键字搜索"),
    dept_name: str | None = Query(None, description="部门"),
    year: int | None = Query(None, description="年份"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页条数"),
):
    """分页查询预算列表"""
    items, total = await budget_service.get_budget_list(keyword, dept_name, year, page, page_size)
    return ApiResponse(data=PageResult(items=items, total=total, page=page, page_size=page_size))


@router.get("/summary", response_model=ApiResponse[BudgetSummary])
async def get_summary():
    """预算统计摘要"""
    data = await budget_service.get_budget_summary()
    return ApiResponse(data=data)


@router.get("/{budget_id}", response_model=ApiResponse[BudgetResponse])
async def get_detail(budget_id: int):
    """预算详情"""
    data = await budget_service.get_budget_detail(budget_id)
    return ApiResponse(data=data)


@router.post("", response_model=ApiResponse[BudgetResponse])
async def create_budget(data: BudgetCreate):
    """新增预算"""
    result = await budget_service.create_budget(data)
    return ApiResponse(data=result)


@router.put("/{budget_id}", response_model=ApiResponse[BudgetResponse])
async def update_budget(budget_id: int, data: BudgetUpdate):
    """编辑预算"""
    result = await budget_service.update_budget(budget_id, data)
    return ApiResponse(data=result)


@router.post("/{budget_id}/adjust", response_model=ApiResponse[BudgetResponse])
async def adjust_budget(budget_id: int, data: BudgetAdjust):
    """预算调整（追加/削减）"""
    result = await budget_service.adjust_budget(budget_id, data)
    return ApiResponse(data=result)


@router.delete("/{budget_id}", response_model=ApiResponse)
async def delete_budget(budget_id: int):
    """删除预算"""
    await budget_service.delete_budget(budget_id)
    return ApiResponse(msg="删除成功")