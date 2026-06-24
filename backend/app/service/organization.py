"""组织权限 业务逻辑层"""
from app.schemas.organization import DeptCreate, DeptUpdate, DeptResponse, UserCreate, UserUpdate, UserResponse


async def get_dept_list() -> list[DeptResponse]: return []
async def create_dept(data: DeptCreate) -> DeptResponse: return DeptResponse(id=0, **data.model_dump())
async def update_dept(id: int, data: DeptUpdate) -> DeptResponse | None: return None
async def delete_dept(id: int) -> bool: return True

async def get_user_list(page: int = 1, page_size: int = 10) -> tuple[list[UserResponse], int]: return [], 0
async def create_user(data: UserCreate) -> UserResponse: return UserResponse(id=0, **data.model_dump())
async def update_user(id: int, data: UserUpdate) -> UserResponse | None: return None
async def delete_user(id: int) -> bool: return True