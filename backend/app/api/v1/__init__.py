"""API v1 路由注册"""
from fastapi import APIRouter
from app.api.v1.workbench import router as workbench_router
from app.api.v1.expense import router as expense_router
from app.api.v1.budget import router as budget_router
from app.api.v1.ai import router as ai_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.notification import router as notification_router
from app.api.v1.organization import router_departments, router_users

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(workbench_router)
api_router.include_router(expense_router)
api_router.include_router(budget_router)
api_router.include_router(ai_router)
api_router.include_router(dashboard_router)
api_router.include_router(notification_router)
api_router.include_router(router_departments)
api_router.include_router(router_users)