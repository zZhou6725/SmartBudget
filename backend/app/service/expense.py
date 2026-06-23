"""费用报销 业务逻辑层（当前返回空占位数据，后续对接数据库）"""
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseSummary


async def get_expense_list(
    keyword: str | None = None,
    category: str | None = None,
    dept_name: str | None = None,
    status: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> tuple[list[ExpenseResponse], int]:
    """分页查询报销列表"""
    # TODO: 数据库查询 + 多条件筛选
    return [], 0


async def get_expense_summary() -> ExpenseSummary:
    """报销统计摘要"""
    # TODO: 数据库聚合统计
    return ExpenseSummary()


async def get_expense_detail(expense_id: int) -> ExpenseResponse | None:
    """报销详情"""
    # TODO: 数据库按ID查询
    return None


async def create_expense(data: ExpenseCreate, applicant: str = "") -> ExpenseResponse:
    """新增报销"""
    # TODO: 生成单号、写入数据库
    return ExpenseResponse(**data.model_dump(), id=0, applicant=applicant)


async def update_expense(expense_id: int, data: ExpenseUpdate) -> ExpenseResponse | None:
    """编辑报销"""
    # TODO: 数据库更新
    return None


async def delete_expense(expense_id: int) -> bool:
    """软删除报销"""
    # TODO: 设置 deleted_at
    return True
