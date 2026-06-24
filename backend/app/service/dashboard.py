"""数据看板 — 真实数据库聚合查询"""
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Expense, Budget
from app.schemas.dashboard import TrendItem, DeptRankItem, CategoryPieItem, BudgetExecItem


async def get_trend(month: str | None = None, dept_name: str | None = None) -> list[TrendItem]:
    db = SessionLocal()
    try:
        q = db.query(
            func.substr(Expense.apply_date, 1, 7).label("m"),
            func.sum(Expense.amount).label("total")
        ).filter(
            Expense.deleted_at.is_(None),
            Expense.status == "approved"
        )
        if month:
            q = q.filter(Expense.apply_date.like(f"{month}%"))
        if dept_name:
            q = q.filter(Expense.dept_name == dept_name)
        rows = q.group_by("m").order_by("m").all()
        return [TrendItem(month=r.m, amount=float(r.total or 0)) for r in rows]
    finally:
        db.close()


async def get_dept_rank(month: str | None = None) -> list[DeptRankItem]:
    db = SessionLocal()
    try:
        base = db.query(
            Expense.dept_name,
            func.sum(Expense.amount).label("total")
        ).filter(
            Expense.deleted_at.is_(None),
            Expense.status == "approved"
        )
        if month:
            base = base.filter(Expense.apply_date.like(f"{month}%"))
        rows = base.group_by(Expense.dept_name).order_by(func.sum(Expense.amount).desc()).all()

        budgets: dict[str, float] = {}
        for b in db.query(Budget).all():
            budgets[b.dept_name] = budgets.get(b.dept_name, 0) + float(b.total_amount or 0)

        result = []
        for r in rows:
            total_budget = budgets.get(r.dept_name, 0)
            usage = round(float(r.total) / total_budget * 100, 1) if total_budget > 0 else 0
            result.append(DeptRankItem(dept_name=r.dept_name, amount=float(r.total or 0), usage_rate=usage))
        return result
    finally:
        db.close()


async def get_category_pie(month: str | None = None, dept_name: str | None = None) -> list[CategoryPieItem]:
    db = SessionLocal()
    try:
        q = db.query(
            Expense.category,
            func.sum(Expense.amount).label("total")
        ).filter(
            Expense.deleted_at.is_(None),
            Expense.status == "approved"
        )
        if month:
            q = q.filter(Expense.apply_date.like(f"{month}%"))
        if dept_name:
            q = q.filter(Expense.dept_name == dept_name)
        rows = q.group_by(Expense.category).all()

        grand_total = sum(float(r.total or 0) for r in rows)
        result = []
        for r in rows:
            amount = float(r.total or 0)
            percent = round(amount / grand_total * 100, 1) if grand_total > 0 else 0
            result.append(CategoryPieItem(category=r.category or "other", amount=amount, percent=percent))
        return result
    finally:
        db.close()


async def get_budget_exec(year: int | None = None) -> list[BudgetExecItem]:
    db = SessionLocal()
    try:
        q = db.query(Budget)
        if year:
            q = q.filter(Budget.year == year)
        budgets = q.all()

        result = []
        for b in budgets:
            used = float(db.query(func.sum(Expense.amount)).filter(
                Expense.dept_name == b.dept_name,
                Expense.status == "approved",
                Expense.deleted_at.is_(None)
            ).scalar() or 0)
            total = float(b.total_amount or 0)
            rate = round(used / total * 100, 1) if total > 0 else 0
            result.append(BudgetExecItem(dept_name=b.dept_name, budget=total, used=used, rate=rate))
        return result
    finally:
        db.close()
