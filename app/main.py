import httpx
from fastapi import FastAPI, HTTPException, Query
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

app = FastAPI()
geolocator = Nominatim(user_agent="geolocation_api")


@app.get("/geolocation")
async def get_geolocation(q: str):
    try:
        location = geolocator.geocode(q)
        if location:
            return {"latitude": location.latitude, "longitude": location.longitude}
        else:
            raise HTTPException(status_code=404, detail="Location not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reverse-geocode/")
async def reverse_geocode(latitude: float, longitude: float):
    try:
        location = geolocator.reverse((latitude, longitude))
        address = location.address
        return {"address": address}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/calculate_distance")
async def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    """
    Calculate the distance between two sets of coordinates using geopy.

    Parameters:
    - lat1: Latitude of the first point
    - lon1: Longitude of the first point
    - lat2: Latitude of the second point
    - lon2: Longitude of the second point

    Returns:
    - distance: Distance between the two points in kilometers
    """

    # Validate coordinates
    if not (-90 <= lat1 <= 90) or not (-180 <= lon1 <= 180) or not (-90 <= lat2 <= 90) or not (-180 <= lon2 <= 180):
        raise HTTPException(status_code=400, detail="Invalid coordinates provided")

    # Calculate distance using geopy
    coordinates_1 = (lat1, lon1)
    coordinates_2 = (lat2, lon2)
    distance_km = geodesic(coordinates_1, coordinates_2).kilometers

    return {"distance": distance_km}


@app.get("/user/ip")
async def get_user_ip():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://ipinfo.io/json")
            data = response.json()
            return {"user_ip": data["ip"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch user IP")


@app.get("/user/ip/{ip_address}")
async def get_lat_lon(ip_address: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://ipinfo.io/{ip_address}/json")
            data = response.json()
            lat_lon = data.get('loc').split(',')
            latitude = float(lat_lon[0])
            longitude = float(lat_lon[1])
            return {"latitude": latitude, "longitude": longitude}
    except Exception as e:
        return {"error": f"Error occurred: {e}"}
