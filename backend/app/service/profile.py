"""个人中心 — 真实数据库查询"""
from app.database import SessionLocal
from app.models import User, Department
from app.core.security import verify_password, hash_password
from app.schemas.profile import ProfileUpdate, PasswordChange, UserProfileResponse


async def get_profile(current_user_id: int) -> UserProfileResponse:
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.id == current_user_id).first()
        if not u:
            return UserProfileResponse(id=current_user_id, username="", role="viewer")
        dept = db.query(Department).filter(Department.id == u.dept_id).first() if u.dept_id else None
        return UserProfileResponse(
            id=u.id, username=u.username, real_name=u.real_name or "",
            email=u.email or "", phone=u.phone or "",
            dept_name=dept.name if dept else "", role=u.role,
        )
    finally:
        db.close()


async def update_profile(current_user_id: int, data: ProfileUpdate) -> UserProfileResponse:
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.id == current_user_id).first()
        if u:
            if data.real_name is not None:
                u.real_name = data.real_name
            if data.email is not None:
                u.email = data.email
            if data.phone is not None:
                u.phone = data.phone
            db.commit()
            db.refresh(u)
        return await get_profile(current_user_id)
    finally:
        db.close()


async def change_password(current_user_id: int, data: PasswordChange) -> bool:
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.id == current_user_id).first()
        if not u or not verify_password(data.old_password, u.password):
            return False
        u.password = hash_password(data.new_password)
        db.commit()
        return True
    finally:
        db.close()