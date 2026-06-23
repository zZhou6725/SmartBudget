"""费用报销 Schema（与前端 types/expense.ts 字段完全对齐）"""
from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    """新增报销（对齐前端 ExpenseForm）"""
    title: str = Field(..., description="报销标题")
    category: str = Field(..., description="报销类型: travel/office/entertainment/transport/other")
    dept_name: str = Field(..., description="所属部门")
    budget_id: int | None = Field(None, description="关联预算ID（可选）")
    amount: float = Field(..., gt=0, description="报销金额(>0)")
    apply_date: str = Field(..., description="申请日期 YYYY-MM-DD")
    remark: str = Field("", description="备注说明")


class ExpenseUpdate(BaseModel):
    """编辑报销（对齐前端 ExpenseForm，所有字段可选）"""
    title: str | None = Field(None, description="报销标题")
    category: str | None = Field(None, description="报销类型")
    dept_name: str | None = Field(None, description="所属部门")
    budget_id: int | None = Field(None, description="关联预算ID")
    amount: float | None = Field(None, gt=0, description="报销金额")
    apply_date: str | None = Field(None, description="申请日期")
    remark: str | None = Field(None, description="备注说明")


class ExpenseResponse(BaseModel):
    """报销记录响应（对齐前端 ExpenseItem）"""
    id: int
    expense_no: str = ""
    title: str
    category: str
    dept_name: str
    budget_id: int | None = None
    budget_name: str = ""
    amount: float
    status: str = "pending"
    applicant: str = ""
    apply_date: str
    remark: str = ""
    attachment_url: str = ""
    created_at: str = ""


class ExpenseSummary(BaseModel):
    """报销统计摘要（对齐前端 ExpenseSummary）"""
    total_amount: float = 0.0
    pending_count: int = 0
    approved_count: int = 0
    rejected_count: int = 0