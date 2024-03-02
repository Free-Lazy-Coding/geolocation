import asyncio

from asyncer import asyncify
from fastapi import HTTPException
from geopy.distance import geodesic

from app.utils.geolocator import geolocator


async def get_distance(address1: str, address2: str) -> dict:
    location1 = await asyncify(geolocator.geocode)(address1)
    await asyncio.sleep(1)
    location2 = await asyncify(geolocator.geocode)(address2)
    if location1 and location2:
        return await calculate_distance(
            lat1=location1.latitude,
            lon1=location1.longitude,
            lat2=location2.latitude,
            lon2=location2.longitude,
        )
    else:
        raise HTTPException(status_code=404, detail="One or both addresses not found")


async def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> dict:
    coordinates_1 = (lat1, lon1)
    coordinates_2 = (lat2, lon2)
    distance = await asyncify(geodesic)(coordinates_1, coordinates_2)
    return {"distance": distance.kilometers}
