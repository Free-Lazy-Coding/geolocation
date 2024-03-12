# tests/test_services/test_user.py

from app.services.user import get_user_ip, get_lat_lon
from fastapi import Request
import httpx
import pytest
from unittest import mock

@pytest.fixture
def mock_request():
    request = mock.Mock(spec=Request)
    request.client.host = "127.0.0.1"
    return request

@pytest.fixture
def mock_httpx_get():
    with mock.patch("httpx.AsyncClient.get") as mock_httpx_get:
        yield mock_httpx_get

@pytest.mark.asyncio
async def test_get_user_ip(mock_request):
    result = await get_user_ip(mock_request)
    assert result == {"ip": "127.0.0.1"}

@pytest.mark.asyncio
async def test_get_lat_lon_successful(mock_httpx_get):
    mock_httpx_get.return_value.json.return_value = {"loc": "40.7128,-74.0060"}

    result = await get_lat_lon("127.0.0.1")

    assert result == {"latitude": 40.7128, "longitude": -74.0060}

@pytest.mark.asyncio
async def test_get_lat_lon_http_error(mock_httpx_get):
    mock_httpx_get.side_effect = httpx.HTTPError("Mocked HTTP error")

    with pytest.raises(httpx.HTTPError) as exc_info:
        await get_lat_lon("127.0.0.1")

    assert str(exc_info.value) == "Mocked HTTP error"
