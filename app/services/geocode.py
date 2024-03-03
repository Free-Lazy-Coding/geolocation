from asyncer import asyncify
from fastapi import HTTPException

from app.utils.geolocator import geolocator


async def geocode_address(q: str) -> dict:
    location = await asyncify(geolocator.geocode)(q)
    if location:
        return {"latitude": location.latitude, "longitude": location.longitude}
    else:
        raise HTTPException(status_code=404, detail="Location not found")


async def reverse_geocode_coordinates(latitude: float, longitude: float) -> dict:
    location = await asyncify(geolocator.reverse)((latitude, longitude))
    if location:
        return {"address": location.address}
    else:
        raise HTTPException(status_code=404, detail="Address not found")
