"""费用报销 业务逻辑层 — 真实数据库查询"""
from datetime import datetime
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Expense
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
    db = SessionLocal()
    try:
        q = db.query(Expense).filter(Expense.deleted_at.is_(None))
        if keyword:
            q = q.filter(Expense.title.contains(keyword) | Expense.expense_no.contains(keyword))
        if category:
            q = q.filter(Expense.category == category)
        if dept_name:
            q = q.filter(Expense.dept_name == dept_name)
        if status:
            q = q.filter(Expense.status == status)
        if start_date:
            q = q.filter(Expense.apply_date >= start_date)
        if end_date:
            q = q.filter(Expense.apply_date <= end_date)
        total = q.count()
        items = q.order_by(Expense.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        result = [_to_response(e) for e in items]
        return result, total
    finally:
        db.close()


async def get_expense_summary() -> ExpenseSummary:
    db = SessionLocal()
    try:
        base = db.query(Expense).filter(Expense.deleted_at.is_(None))
        total_amount = base.with_entities(func.sum(Expense.amount)).scalar() or 0
        pending = base.filter(Expense.status == "pending").count()
        approved = base.filter(Expense.status == "approved").count()
        rejected = base.filter(Expense.status == "rejected").count()
        return ExpenseSummary(total_amount=float(total_amount), pending_count=pending, approved_count=approved, rejected_count=rejected)
    finally:
        db.close()


async def get_expense_detail(expense_id: int) -> ExpenseResponse | None:
    db = SessionLocal()
    try:
        e = db.query(Expense).filter(Expense.id == expense_id, Expense.deleted_at.is_(None)).first()
        return _to_response(e) if e else None
    finally:
        db.close()


async def create_expense(data: ExpenseCreate, applicant: str = "") -> ExpenseResponse:
    db = SessionLocal()
    try:
        today = datetime.now().strftime("%Y%m%d")
        e = Expense(expense_no=f"E{today}{datetime.now().strftime('%H%M%S')}", applicant=applicant, **data.model_dump())
        db.add(e)
        db.commit()
        db.refresh(e)
        return _to_response(e)
    finally:
        db.close()


async def update_expense(expense_id: int, data: ExpenseUpdate) -> ExpenseResponse | None:
    db = SessionLocal()
    try:
        e = db.query(Expense).filter(Expense.id == expense_id, Expense.deleted_at.is_(None)).first()
        if not e:
            return None
        for k, v in data.model_dump(exclude_none=True).items():
            setattr(e, k, v)
        db.commit()
        db.refresh(e)
        return _to_response(e)
    finally:
        db.close()


async def delete_expense(expense_id: int) -> bool:
    db = SessionLocal()
    try:
        e = db.query(Expense).filter(Expense.id == expense_id).first()
        if e:
            e.deleted_at = datetime.utcnow()
            db.commit()
        return True
    finally:
        db.close()


def _to_response(e: Expense) -> ExpenseResponse:
    return ExpenseResponse(
        id=e.id, expense_no=e.expense_no or "", title=e.title, category=e.category or "other",
        dept_name=e.dept_name, budget_id=e.budget_id, budget_name="",
        amount=float(e.amount), status=e.status or "pending", applicant=e.applicant or "",
        apply_date=e.apply_date or "", remark=e.remark or "", attachment_url=e.attachment_url or "",
        created_at=str(e.created_at)[:19] if e.created_at else "",
    )