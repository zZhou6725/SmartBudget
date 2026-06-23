"""全局异常处理"""
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.response import ApiResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """参数校验异常 → 统一返回体"""
    return JSONResponse(
        status_code=422,
        content=ApiResponse(code=422, data=None, msg=str(exc)).model_dump(),
    )


async def global_exception_handler(request: Request, exc: Exception):
    """未知异常 → 统一返回体"""
    return JSONResponse(
        status_code=500,
        content=ApiResponse(code=500, data=None, msg="服务器内部错误").model_dump(),
    )