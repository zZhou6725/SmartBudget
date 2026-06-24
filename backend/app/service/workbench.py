"""工作台 业务逻辑层 — 真实数据查询"""
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Budget, Expense


async def get_overview() -> dict:
    """概览统计"""
    db = SessionLocal()
    try:
        total_budget = db.query(func.sum(Budget.total_amount)).scalar() or 0
        total_expense = db.query(func.sum(Expense.amount)).filter(Expense.status == "approved").scalar() or 0
        pending = db.query(func.count(Expense.id)).filter(Expense.status == "pending").scalar() or 0
        # 超预算部门：按部门统计支出超过该部门预算的部门数
        dept_budgets = dict(db.query(Budget.dept_name, func.sum(Budget.total_amount)).group_by(Budget.dept_name).all())
        dept_expenses = dict(db.query(Expense.dept_name, func.sum(Expense.amount)).group_by(Expense.dept_name).all())
        over_budget = sum(1 for d, b in dept_budgets.items() if dept_expenses.get(d, 0) > b)
        return {
            "total_budget": float(total_budget),
            "total_expense": float(total_expense),
            "remaining_balance": float(total_budget - total_expense),
            "pending_approvals": pending,
            "over_budget_depts": over_budget,
        }
    finally:
        db.close()


async def get_pending_approvals(page: int = 1, page_size: int = 10) -> tuple[list[dict], int]:
    """待审批列表"""
    db = SessionLocal()
    try:
        total = db.query(func.count(Expense.id)).filter(Expense.status == "pending").scalar() or 0
        items = db.query(Expense).filter(Expense.status == "pending").order_by(Expense.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        result = [{
            "id": e.id, "title": e.title, "applicant": e.applicant or "",
            "amount": float(e.amount), "time": str(e.created_at)[:10], "status": e.status or "",
        } for e in items]
        return result, total
    finally:
        db.close()


async def get_expense_trend() -> list[dict]:
    """支出趋势（近6个月）"""
    db = SessionLocal()
    try:
        rows = db.query(
            func.date_format(Expense.created_at, "%Y-%m").label("month"),
            func.sum(Expense.amount).label("amount"),
        ).filter(Expense.status == "approved").group_by("month").order_by("month").limit(12).all()
        return [{"date": r[0], "amount": float(r[1] or 0)} for r in rows]
    finally:
        db.close()