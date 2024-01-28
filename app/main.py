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
