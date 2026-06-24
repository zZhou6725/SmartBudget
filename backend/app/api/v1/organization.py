"""组织权限 API（/api/v1/departments + /api/v1/users）"""
from fastapi import APIRouter, Query

from app.core.response import ApiResponse, PageResult
from app.schemas.organization import DeptCreate, DeptUpdate, DeptResponse, UserCreate, UserUpdate, UserResponse
from app.service import organization as org_service

router_departments = APIRouter(prefix="/departments", tags=["部门管理"])
router_users = APIRouter(prefix="/users", tags=["用户管理"])


@router_departments.get("", response_model=ApiResponse[list[DeptResponse]])
async def list_depts(): return ApiResponse(data=await org_service.get_dept_list())

@router_departments.post("", response_model=ApiResponse[DeptResponse])
async def create_dept(data: DeptCreate): return ApiResponse(data=await org_service.create_dept(data))

@router_departments.put("/{dept_id}", response_model=ApiResponse[DeptResponse])
async def update_dept(dept_id: int, data: DeptUpdate): return ApiResponse(data=await org_service.update_dept(dept_id, data))

@router_departments.delete("/{dept_id}", response_model=ApiResponse)
async def delete_dept(dept_id: int): await org_service.delete_dept(dept_id); return ApiResponse(msg="删除成功")


@router_users.get("", response_model=ApiResponse[PageResult[UserResponse]])
async def list_users(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    items, total = await org_service.get_user_list(page, page_size)
    return ApiResponse(data=PageResult(items=items, total=total, page=page, page_size=page_size))

@router_users.post("", response_model=ApiResponse[UserResponse])
async def create_user(data: UserCreate): return ApiResponse(data=await org_service.create_user(data))

@router_users.put("/{user_id}", response_model=ApiResponse[UserResponse])
async def update_user(user_id: int, data: UserUpdate): return ApiResponse(data=await org_service.update_user(user_id, data))

@router_users.delete("/{user_id}", response_model=ApiResponse)
async def delete_user(user_id: int): await org_service.delete_user(user_id); return ApiResponse(msg="删除成功")