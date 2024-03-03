import functools
import json
import inspect
import os

import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL", default="redis://localhost:6379")
redis_connection = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)


def cache_key_generator(endpoint, *args, **kwargs):
    return f"{endpoint.__name__}:{args}:{kwargs}"


async def get_cached_or_fetch(key, func, *args, **kwargs):
    cached_data = await redis_connection.get(key)

    if cached_data:
        return json.loads(cached_data)
    else:
        if inspect.iscoroutinefunction(func):
            result = await func(*args, **kwargs)
        else:
            result = func(*args, **kwargs)

        serialized_result = json.dumps(result)
        await redis_connection.setex(key, 3600, serialized_result)  # Cache for 1 hour
        return result


def cache_response():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = cache_key_generator(func, *args, **kwargs)
            return await get_cached_or_fetch(key, func, *args, **kwargs)
        return wrapper
    return decorator
