import asyncio
import inspect
import json
import os

import redis.asyncio as redis
import httpx
from fastapi import FastAPI, HTTPException, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

app = FastAPI()
geolocator = Nominatim(user_agent="geolocation_api")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_connection = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)


@app.on_event("startup")
async def startup():
    await FastAPILimiter.init(redis_connection)


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
        if hasattr(result, 'latitude') and hasattr(result, 'longitude'):
            serialized_result = {"latitude": result.latitude, "longitude": result.longitude}
            await redis_connection.setex(key, 3600, json.dumps(serialized_result))  # Cache for 1 hour
            return serialized_result
        else:
            serialized_result = json.dumps(result)
            await redis_connection.setex(key, 3600, serialized_result)  # Cache for 1 hour
            return result


@app.get("/geolocation", dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def get_geolocation(q: str):
    try:
        key = cache_key_generator(get_geolocation, q)
        return await get_cached_or_fetch(key, geolocator.geocode, q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reverse-geocode/", dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def reverse_geocode(latitude: float, longitude: float):
    try:
        key = cache_key_generator(reverse_geocode, latitude, longitude)
        return await get_cached_or_fetch(key, geolocator.reverse, (latitude, longitude))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/calculate_distance", dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    try:
        key = cache_key_generator(calculate_distance, lat1, lon1, lat2, lon2)
        return await get_cached_or_fetch(key, _calculate_distance, lat1, lon1, lat2, lon2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    coordinates_1 = (lat1, lon1)
    coordinates_2 = (lat2, lon2)
    distance_km = geodesic(coordinates_1, coordinates_2).kilometers
    return {"distance": distance_km}


@app.get("/distance", dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def get_distance(address1: str, address2: str):
    try:
        key = cache_key_generator(get_distance, address1, address2)
        return await get_cached_or_fetch(key, _get_distance, address1, address2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _get_distance(address1: str, address2: str):
    location1 = geolocator.geocode(address1)
    await asyncio.sleep(1)  # Introduce a 1-second delay
    location2 = geolocator.geocode(address2)

    if not location1 or not location2:
        raise HTTPException(status_code=404, detail="One or both addresses not found")

    coords1 = (location1.latitude, location1.longitude)
    coords2 = (location2.latitude, location2.longitude)
    distance_km = geodesic(coords1, coords2).kilometers

    return {"distance_km": distance_km}


@app.get("/user/ip", dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def get_user_ip():
    try:
        key = cache_key_generator(get_user_ip)
        return await get_cached_or_fetch(key, _get_user_ip)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _get_user_ip():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://ipinfo.io/json")
        data = response.json()
        return {"user_ip": data["ip"]}


@app.get("/user/ip/{ip_address}", dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def get_lat_lon(ip_address: str):
    try:
        key = cache_key_generator(get_lat_lon, ip_address)
        return await get_cached_or_fetch(key, _get_lat_lon, ip_address)
    except Exception as e:
        return {"error": f"Error occurred: {e}"}


async def _get_lat_lon(ip_address: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://ipinfo.io/{ip_address}/json")
        data = response.json()
        lat_lon = data.get('loc').split(',')
        latitude = float(lat_lon[0])
        longitude = float(lat_lon[1])
        return {"latitude": latitude, "longitude": longitude}
