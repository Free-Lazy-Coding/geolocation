import json

import pytest
from app.utils.cache import get_cached_or_fetch, cache_response


@pytest.mark.asyncio
async def test_get_cached_or_fetch_async(mock_redis):
    async def mock_async_func(*args, **kwargs):
        return {"result": "async data"}

    # Test with cached data
    mock_redis.get.return_value = json.dumps({"cached": "data"})
    key = "test_key_async"
    result = await get_cached_or_fetch(key, mock_async_func, 1, param="test")
    assert result == {"cached": "data"}

    # Test without cached data
    mock_redis.get.return_value = None
    result = await get_cached_or_fetch(key, mock_async_func, 1, param="test")
    assert result == {"result": "async data"}


@pytest.mark.asyncio
async def test_get_cached_or_fetch_sync(mock_redis):
    def mock_sync_func(*args, **kwargs):
        return {"result": "sync data"}

    # Test with cached data - synchronous function
    mock_redis.get.return_value = json.dumps({"cached": "data"})
    key = "test_key_sync"
    result = await get_cached_or_fetch(key, mock_sync_func, 1, param="test")
    assert result == {"cached": "data"}

    # Test without cached data - synchronous function
    mock_redis.get.return_value = None
    result = await get_cached_or_fetch(key, mock_sync_func, 1, param="test")
    assert result == {"result": "sync data"}


@pytest.mark.asyncio
async def test_cache_response(mock_redis):
    async def async_func(*args, **kwargs):
        return {"result": "async data"}

    # Test with cached data
    mock_redis.get.return_value = json.dumps({"cached": "data"})
    decorated_func = cache_response()(async_func)
    result = await decorated_func(1, param="test")
    assert result == {"cached": "data"}

    # Test without cached data
    mock_redis.get.return_value = None
    result = await decorated_func(1, param="test")
    assert result == {"result": "async data"}

