import httpx
from fastapi import Request, HTTPException


async def get_user_ip(request: Request) -> dict:
    host = request.headers.get('X-Forwarded-For') or request.client.host
    return {"ip": host}


async def get_lat_lon(ip_address: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://ipinfo.io/{ip_address}/json")
        data = response.json()
        if "error" in data:
            error_message = data["error"]["message"]
            raise HTTPException(status_code=404, detail=error_message)

        lat_lon = data.get('loc').split(',')
        latitude = float(lat_lon[0])
        longitude = float(lat_lon[1])
        return {"latitude": latitude, "longitude": longitude}
