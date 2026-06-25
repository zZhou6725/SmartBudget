"""组织权限 — 真实数据库查询"""
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Department, User, Budget
from app.core.security import hash_password
from app.schemas.organization import DeptCreate, DeptUpdate, DeptResponse, UserCreate, UserUpdate, UserResponse


async def get_dept_list() -> list[DeptResponse]:
    db = SessionLocal()
    try:
        depts = db.query(Department).all()
        if not depts:
            return []

        # batch query member counts
        dept_ids = [d.id for d in depts]
        member_rows = db.query(
            User.dept_id, func.count(User.id)
        ).filter(User.dept_id.in_(dept_ids)).group_by(User.dept_id).all()
        member_map = {r[0]: r[1] for r in member_rows}

        # batch query budgets
        dept_names = [d.name for d in depts]
        budget_rows = db.query(
            Budget.dept_name, func.sum(Budget.total_amount)
        ).filter(Budget.dept_name.in_(dept_names)).group_by(Budget.dept_name).all()
        budget_map = {r[0]: float(r[1] or 0) for r in budget_rows}

        result = []
        for d in depts:
            result.append(DeptResponse(
                id=d.id,
                name=d.name,
                manager=d.manager or "",
                member_count=member_map.get(d.id, 0),
                total_budget=budget_map.get(d.name, 0.0),
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
        if not users:
            return [], total

        dept_ids = list({u.dept_id for u in users if u.dept_id})
        depts = db.query(Department).filter(Department.id.in_(dept_ids)).all() if dept_ids else []
        dept_map = {d.id: d.name for d in depts}

        result = []
        for u in users:
            result.append(UserResponse(
                id=u.id,
                username=u.username,
                real_name=u.real_name or "",
                dept_name=dept_map.get(u.dept_id, "") if u.dept_id else "",
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