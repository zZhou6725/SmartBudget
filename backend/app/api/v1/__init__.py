"""API v1 路由注册"""
from fastapi import APIRouter
from app.api.v1.workbench import router as workbench_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(workbench_router)