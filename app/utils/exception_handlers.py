from fastapi import Request
from fastapi.responses import JSONResponse


async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
