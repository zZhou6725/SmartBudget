"""个人中心 API（/api/v1/profile）"""
from fastapi import APIRouter, Depends

from app.core.response import ApiResponse
from app.core.deps import get_current_user
from app.schemas.profile import ProfileUpdate, PasswordChange, UserProfileResponse
from app.service import profile as profile_service

router = APIRouter(prefix="/profile", tags=["个人中心"])


@router.get("", response_model=ApiResponse[UserProfileResponse])
async def get_profile(user=Depends(get_current_user)):
    return ApiResponse(data=await profile_service.get_profile(user["user_id"]))

@router.put("", response_model=ApiResponse[UserProfileResponse])
async def update_profile(data: ProfileUpdate, user=Depends(get_current_user)):
    return ApiResponse(data=await profile_service.update_profile(user["user_id"], data))

@router.put("/password", response_model=ApiResponse)
async def change_password(data: PasswordChange, user=Depends(get_current_user)):
    ok = await profile_service.change_password(user["user_id"], data)
    if not ok:
        return ApiResponse(code=400, msg="原密码错误")
    return ApiResponse(msg="密码修改成功")