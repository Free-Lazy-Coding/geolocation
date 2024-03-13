from asyncer import asyncify
from fastapi import HTTPException
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

from app.utils.geolocator import geolocator


async def geocode_address(q: str) -> dict:
    try:
        location = await asyncify(geolocator.geocode)(q)
    except (GeocoderTimedOut, GeocoderUnavailable):  # Handle GeocoderTimedOut exception
        raise HTTPException(status_code=503, detail="Geocoding service timed out")  # Return appropriate response
    if location:
        return {"latitude": location.latitude, "longitude": location.longitude}
    else:
        raise HTTPException(status_code=404, detail="Location not found")


async def reverse_geocode_coordinates(latitude: float, longitude: float) -> dict:
    try:
        location = await asyncify(geolocator.reverse)((latitude, longitude))
    except (GeocoderTimedOut, GeocoderUnavailable):  # Handle GeocoderTimedOut exception
        raise HTTPException(status_code=503, detail="Geocoding service timed out")  # Return appropriate response
    if location:
        return {"address": location.address}
    else:
        raise HTTPException(status_code=404, detail="Address not found")
