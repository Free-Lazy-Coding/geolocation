import pytest
from fastapi import HTTPException, Request

from app.utils.exception_handlers import custom_exception_handler


@pytest.mark.asyncio
async def test_custom_exception_handler():
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": "/",
        "query_string": b"",
        "headers": [],
    }
    request = Request(scope=scope)

    # Test for HTTPException
    http_exception = HTTPException(status_code=500, detail="Check error")
    response = await custom_exception_handler(request, http_exception)
    assert response.status_code == 500

    # Test for other exceptions
    other_exception = ValueError("Something went wrong")
    response = await custom_exception_handler(request, other_exception)
    assert response.status_code == 500
