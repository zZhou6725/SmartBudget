"""预算管理 — 真实数据库查询"""
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Budget, Expense
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetAdjust, BudgetResponse, BudgetSummary


async def get_budget_list(keyword=None, dept_name=None, year=None, page=1, page_size=10):
    db = SessionLocal()
    try:
        q = db.query(Budget)
        if keyword: q = q.filter(Budget.dept_name.contains(keyword))
        if dept_name: q = q.filter(Budget.dept_name == dept_name)
        if year: q = q.filter(Budget.year == year)
        total = q.count()
        items = q.order_by(Budget.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return [_to_response(e) for e in items], total
    finally:
        db.close()


async def get_budget_summary():
    db = SessionLocal()
    try:
        total_budget = float(db.query(func.sum(Budget.total_amount)).scalar() or 0)
        total_used = float(db.query(func.sum(Expense.amount)).filter(Expense.status == "approved").scalar() or 0)
        remaining = total_budget - total_used
        rate = int(total_used / total_budget * 100) if total_budget > 0 else 0
        return BudgetSummary(total_budget=total_budget, total_used=total_used, total_remaining=remaining, avg_usage_rate=rate)
    finally:
        db.close()


async def get_budget_detail(budget_id: int):
    db = SessionLocal()
    try:
        b = db.query(Budget).filter(Budget.id == budget_id).first()
        return _to_response(b) if b else None
    finally:
        db.close()


async def create_budget(data: BudgetCreate):
    db = SessionLocal()
    try:
        b = Budget(**data.model_dump())
        db.add(b); db.commit(); db.refresh(b)
        return _to_response(b)
    finally:
        db.close()


async def update_budget(budget_id: int, data: BudgetUpdate):
    db = SessionLocal()
    try:
        b = db.query(Budget).filter(Budget.id == budget_id).first()
        if not b: return None
        for k, v in data.model_dump(exclude_none=True).items(): setattr(b, k, v)
        db.commit(); db.refresh(b)
        return _to_response(b)
    finally:
        db.close()


async def adjust_budget(budget_id: int, data: BudgetAdjust):
    db = SessionLocal()
    try:
        b = db.query(Budget).filter(Budget.id == budget_id).first()
        if not b: return None
        delta = data.amount if data.direction == "add" else -data.amount
        b.total_amount = max(0, (b.total_amount or 0) + delta)
        db.commit(); db.refresh(b)
        return _to_response(b)
    finally:
        db.close()


async def delete_budget(budget_id: int):
    db = SessionLocal()
    try:
        b = db.query(Budget).filter(Budget.id == budget_id).first()
        if b: db.delete(b); db.commit()
        return True
    finally:
        db.close()


def _to_response(b: Budget) -> BudgetResponse:
    used = float(SessionLocal().query(func.sum(Expense.amount)).filter(Expense.status == "approved", Expense.dept_name == b.dept_name).scalar() or 0)
    remaining = (b.total_amount or 0) - used
    rate = int(used / b.total_amount * 100) if b.total_amount else 0
    return BudgetResponse(
        id=b.id, dept_name=b.dept_name, year=b.year or 0,
        total_amount=float(b.total_amount or 0), used_amount=used,
        remaining=remaining, usage_rate=rate,
        created_at=str(b.created_at)[:19] if b.created_at else "",
    )
