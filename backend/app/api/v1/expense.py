"""费用报销 API 路由（GET/POST/PUT/DELETE /api/v1/expenses）"""
from fastapi import APIRouter, Query

from app.core.response import ApiResponse, PageResult
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseSummary
from app.service import expense as expense_service

router = APIRouter(prefix="/expenses", tags=["费用报销"])


@router.get("", response_model=ApiResponse[PageResult[ExpenseResponse]])
async def list_expenses(
    keyword: str | None = Query(None, description="关键字搜索"),
    category: str | None = Query(None, description="报销类型"),
    dept_name: str | None = Query(None, description="部门"),
    status: str | None = Query(None, description="状态"),
    start_date: str | None = Query(None, description="开始日期"),
    end_date: str | None = Query(None, description="结束日期"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页条数"),
):
    """分页查询报销列表"""
    items, total = await expense_service.get_expense_list(
        keyword, category, dept_name, status, start_date, end_date, page, page_size
    )
    return ApiResponse(data=PageResult(items=items, total=total, page=page, page_size=page_size))


@router.get("/summary", response_model=ApiResponse[ExpenseSummary])
async def get_summary():
    """报销统计摘要"""
    data = await expense_service.get_expense_summary()
    return ApiResponse(data=data)


@router.get("/{expense_id}", response_model=ApiResponse[ExpenseResponse])
async def get_detail(expense_id: int):
    """报销详情"""
    data = await expense_service.get_expense_detail(expense_id)
    return ApiResponse(data=data)


@router.post("", response_model=ApiResponse[ExpenseResponse])
async def create_expense(data: ExpenseCreate):
    """新增报销"""
    result = await expense_service.create_expense(data)
    return ApiResponse(data=result)


@router.put("/{expense_id}", response_model=ApiResponse[ExpenseResponse])
async def update_expense(expense_id: int, data: ExpenseUpdate):
    """编辑报销"""
    result = await expense_service.update_expense(expense_id, data)
    return ApiResponse(data=result)


@router.delete("/{expense_id}", response_model=ApiResponse)
async def delete_expense(expense_id: int):
    """删除报销（软删除）"""
    await expense_service.delete_expense(expense_id)
    return ApiResponse(msg="删除成功")