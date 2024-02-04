import httpx
from fastapi import FastAPI, HTTPException
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
