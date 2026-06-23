"""工作台 Schema（与前端 types/workbench.ts 字段完全对齐）"""
from pydantic import BaseModel


class WorkbenchOverview(BaseModel):
    """概览统计数据（对齐前端 WorkbenchOverview）"""
    total_budget: float | None = None      # 总预算
    total_expense: float | None = None     # 总支出
    remaining_balance: float | None = None # 剩余余额
    pending_approvals: int | None = None   # 待审批数
    over_budget_depts: int | None = None   # 超预算部门数


class PendingApprovalItem(BaseModel):
    """待审批事项（对齐前端 PendingApprovalItem）"""
    id: int                          # 主键ID
    title: str                       # 审批标题
    applicant: str                   # 申请人
    amount: float                    # 金额
    time: str                        # 提交时间
    status: str                      # 状态


class TrendPoint(BaseModel):
    """支出趋势数据点（对齐前端 TrendPoint）"""
    date: str                        # 日期
    amount: float                    # 金额