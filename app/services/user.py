import httpx
from fastapi import Request


async def get_user_ip(request: Request) -> dict:
    return {"ip": request.client.host}


async def get_lat_lon(ip_address: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://ipinfo.io/{ip_address}/json")
        data = response.json()
        lat_lon = data.get('loc').split(',')
        latitude = float(lat_lon[0])
        longitude = float(lat_lon[1])
        return {"latitude": latitude, "longitude": longitude}
