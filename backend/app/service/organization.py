"""组织权限 — 真实数据库查询"""
from app.database import SessionLocal
from app.models import Department, User, Budget
from app.core.security import hash_password
from app.schemas.organization import DeptCreate, DeptUpdate, DeptResponse, UserCreate, UserUpdate, UserResponse


async def get_dept_list() -> list[DeptResponse]:
    db = SessionLocal()
    try:
        depts = db.query(Department).all()
        result = []
        for d in depts:
            member_count = db.query(User).filter(User.dept_id == d.id).count()
            total_budget = db.query(Budget).filter(Budget.dept_name == d.name).first()
            budget_amount = float(total_budget.total_amount or 0) if total_budget else 0.0
            result.append(DeptResponse(
                id=d.id,
                name=d.name,
                manager=d.manager or "",
                member_count=member_count,
                total_budget=budget_amount,
            ))
        return result
    finally:
        db.close()


async def create_dept(data: DeptCreate) -> DeptResponse:
    db = SessionLocal()
    try:
        d = Department(name=data.name, manager=data.manager)
        db.add(d)
        db.commit()
        db.refresh(d)
        return DeptResponse(id=d.id, name=d.name, manager=d.manager or "")
    finally:
        db.close()


async def update_dept(id: int, data: DeptUpdate) -> DeptResponse | None:
    db = SessionLocal()
    try:
        d = db.query(Department).filter(Department.id == id).first()
        if not d:
            return None
        for k, v in data.model_dump(exclude_none=True).items():
            setattr(d, k, v)
        db.commit()
        db.refresh(d)
        return DeptResponse(id=d.id, name=d.name, manager=d.manager or "")
    finally:
        db.close()


async def delete_dept(id: int) -> bool:
    db = SessionLocal()
    try:
        d = db.query(Department).filter(Department.id == id).first()
        if d:
            db.delete(d)
            db.commit()
        return True
    finally:
        db.close()


async def get_user_list(page: int = 1, page_size: int = 10) -> tuple[list[UserResponse], int]:
    db = SessionLocal()
    try:
        q = db.query(User)
        total = q.count()
        users = q.order_by(User.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
        result = []
        for u in users:
            dept = db.query(Department).filter(Department.id == u.dept_id).first() if u.dept_id else None
            result.append(UserResponse(
                id=u.id,
                username=u.username,
                real_name=u.real_name or "",
                dept_name=dept.name if dept else "",
                role=u.role,
                status=u.status,
            ))
        return result, total
    finally:
        db.close()


async def create_user(data: UserCreate) -> UserResponse:
    db = SessionLocal()
    try:
        u = User(
            username=data.username,
            real_name=data.real_name,
            dept_id=data.dept_id,
            role=data.role,
            password=hash_password("123456"),
        )
        db.add(u)
        db.commit()
        db.refresh(u)
        dept = db.query(Department).filter(Department.id == u.dept_id).first() if u.dept_id else None
        return UserResponse(
            id=u.id, username=u.username, real_name=u.real_name or "",
            dept_name=dept.name if dept else "", role=u.role, status=u.status,
        )
    finally:
        db.close()


async def update_user(id: int, data: UserUpdate) -> UserResponse | None:
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.id == id).first()
        if not u:
            return None
        for k, v in data.model_dump(exclude_none=True).items():
            setattr(u, k, v)
        db.commit()
        db.refresh(u)
        dept = db.query(Department).filter(Department.id == u.dept_id).first() if u.dept_id else None
        return UserResponse(
            id=u.id, username=u.username, real_name=u.real_name or "",
            dept_name=dept.name if dept else "", role=u.role, status=u.status,
        )
    finally:
        db.close()


async def delete_user(id: int) -> bool:
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.id == id).first()
        if u:
            db.delete(u)
            db.commit()
        return True
    finally:
        db.close()