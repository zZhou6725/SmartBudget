"""预算管理 Schema（与前端 types/budget.ts 字段完全对齐）"""
from pydantic import BaseModel, Field


class BudgetCreate(BaseModel):
    """新增预算（对齐前端 BudgetForm）"""
    dept_name: str = Field(..., description="部门名称")
    year: int = Field(..., description="预算年份")
    total_amount: float = Field(..., gt=0, description="预算总额(>0)")


class BudgetUpdate(BaseModel):
    """编辑预算（对齐前端 BudgetForm）"""
    dept_name: str | None = Field(None, description="部门名称")
    year: int | None = Field(None, description="预算年份")
    total_amount: float | None = Field(None, gt=0, description="预算总额")


class BudgetAdjust(BaseModel):
    """预算调整（对齐前端 BudgetAdjustForm）"""
    direction: str = Field(..., description="调整方向: add/subtract")
    amount: float = Field(..., gt=0, description="调整金额(>0)")
    reason: str = Field("", description="调整原因")


class BudgetResponse(BaseModel):
    """预算记录响应（对齐前端 BudgetItem）"""
    id: int
    dept_name: str
    year: int
    total_amount: float
    used_amount: float = 0.0
    remaining: float = 0.0
    usage_rate: int = 0
    created_at: str = ""


class BudgetSummary(BaseModel):
    """预算统计摘要（对齐前端 BudgetSummary）"""
    total_budget: float = 0.0
    total_used: float = 0.0
    total_remaining: float = 0.0
    avg_usage_rate: int = 0