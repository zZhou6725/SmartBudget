"""个人中心 API（/api/v1/profile）"""
from fastapi import APIRouter

from app.core.response import ApiResponse
from app.schemas.profile import ProfileUpdate, PasswordChange, UserProfileResponse
from app.service import profile as profile_service

router = APIRouter(prefix="/profile", tags=["个人中心"])

FAKE_USER_ID = 1  # TODO: 替换为 JWT 鉴权后的当前用户ID


@router.get("", response_model=ApiResponse[UserProfileResponse])
async def get_profile(): return ApiResponse(data=await profile_service.get_profile(FAKE_USER_ID))

@router.put("", response_model=ApiResponse[UserProfileResponse])
async def update_profile(data: ProfileUpdate): return ApiResponse(data=await profile_service.update_profile(FAKE_USER_ID, data))

@router.put("/password", response_model=ApiResponse)
async def change_password(data: PasswordChange):
    ok = await profile_service.change_password(FAKE_USER_ID, data)
    if not ok:
        return ApiResponse(code=400, msg="原密码错误")
    return ApiResponse(msg="密码修改成功")