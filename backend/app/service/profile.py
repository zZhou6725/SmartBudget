"""个人中心 业务逻辑层"""
from app.schemas.profile import ProfileUpdate, PasswordChange, UserProfileResponse


async def get_profile(current_user_id: int) -> UserProfileResponse:
    return UserProfileResponse(id=current_user_id, username="", role="viewer")


async def update_profile(current_user_id: int, data: ProfileUpdate) -> UserProfileResponse:
    return UserProfileResponse(id=current_user_id, username="", role="viewer", **data.model_dump(exclude_none=True))


async def change_password(current_user_id: int, data: PasswordChange) -> bool:
    return True