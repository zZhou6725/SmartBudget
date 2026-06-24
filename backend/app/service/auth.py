"""鉴权 业务逻辑层"""
from app.core.security import hash_password, verify_password, create_access_token


async def login(username: str, password: str) -> dict | None:
    # TODO: 从 users 表查询用户，验证密码
    return {
        "token": create_access_token(1, username),
        "user_info": {"id": 1, "username": username, "real_name": "", "avatar": "", "role": "viewer"},
    }


async def get_user_info(user_id: int) -> dict:
    # TODO: 从 users 表查询
    return {"id": user_id, "username": "", "real_name": "", "avatar": "", "role": "viewer"}