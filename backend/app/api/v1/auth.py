"""鉴权 API（/api/v1/auth）"""
from fastapi import APIRouter, Depends

from app.core.response import ApiResponse
from app.core.deps import get_current_user
from app.schemas.auth import LoginRequest, LoginResponse
from app.service import auth as auth_service

router = APIRouter(prefix="/auth", tags=["鉴权"])


@router.post("/login", response_model=ApiResponse[LoginResponse])
async def login(data: LoginRequest):
    result = await auth_service.login(data.username, data.password)
    if not result:
        return ApiResponse(code=401, msg="用户名或密码错误")
    return ApiResponse(data=LoginResponse(**result))


@router.get("/me")
async def me(user=Depends(get_current_user)):
    info = await auth_service.get_user_info(user["user_id"])
    return ApiResponse(data=info)