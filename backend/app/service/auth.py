"""鉴权 — 真实数据库查询"""
from app.database import SessionLocal
from app.models import User, Department
from app.core.security import verify_password, create_access_token


async def login(username: str, password: str) -> dict | None:
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.username == username, User.status == "active").first()
        if not u or not verify_password(password, u.password):
            return None
        dept = db.query(Department).filter(Department.id == u.dept_id).first() if u.dept_id else None
        return {
            "token": create_access_token(u.id, u.username),
            "user_info": {
                "id": u.id,
                "username": u.username,
                "real_name": u.real_name or "",
                "avatar": "",
                "role": u.role,
                "dept_name": dept.name if dept else "",
            },
        }
    finally:
        db.close()


async def get_user_info(user_id: int) -> dict:
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.id == user_id).first()
        if not u:
            return {}
        dept = db.query(Department).filter(Department.id == u.dept_id).first() if u.dept_id else None
        return {
            "id": u.id,
            "username": u.username,
            "real_name": u.real_name or "",
            "avatar": "",
            "role": u.role,
            "dept_name": dept.name if dept else "",
        }
    finally:
        db.close()