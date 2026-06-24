"""依赖注入 — 从 JWT 解析当前用户"""
from fastapi import Depends, HTTPException, Header
from app.core.security import decode_access_token


async def get_current_user(authorization: str = Header(default="")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登录或Token无效")
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token已过期或无效")
    return {"user_id": int(payload["sub"]), "username": payload["username"]}