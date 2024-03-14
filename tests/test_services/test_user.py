import httpx
import pytest
from unittest import mock

from app.services.user import get_user_ip, get_lat_lon


@pytest.mark.asyncio
async def test_get_user_ip(mock_request):
    result = await get_user_ip(mock_request)
    assert result == {"ip": "127.0.0.1"}


@pytest.mark.asyncio
async def test_get_lat_lon_successful(mock_httpx_get):
    mock_response = mock.MagicMock()
    mock_response.json.return_value = {"loc": "40.7128,-74.0060"}
    mock_httpx_get.return_value = mock_response

    result = await get_lat_lon("8.8.8.8")

    assert result == {"latitude": 40.7128, "longitude": -74.0060}


@pytest.mark.asyncio
async def test_get_lat_lon_http_error(mock_httpx_get):
    mock_httpx_get.side_effect = httpx.HTTPError("Mocked HTTP error")

    with pytest.raises(httpx.HTTPError) as exc_info:
        await get_lat_lon("127.0.0.1")

    assert str(exc_info.value) == "Mocked HTTP error"
