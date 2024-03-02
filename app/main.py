from fastapi import Depends, FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from app.endpoints.distance import router as distance_router
from app.endpoints.geocode import router as geocode_router
from app.endpoints.user import router as user_router
from app.utils.cache import redis_connection
from app.utils.exception_handlers import custom_exception_handler

app = FastAPI(
    title="Geolocation API",
    description="API for geolocation services, including distance calculation, geocoding, and IP-related information.",
    version="1.0.0",
    dependencies=[Depends(RateLimiter(times=1, seconds=2))],
)

app.add_exception_handler(Exception, custom_exception_handler)


@app.on_event("startup")
async def startup():
    await FastAPILimiter.init(redis_connection)


@app.on_event("shutdown")
async def shutdown():
    await FastAPILimiter.close()

app.include_router(distance_router, prefix="/distance", tags=["Distance"])
app.include_router(geocode_router, prefix="/geocode", tags=["Geocode"])
app.include_router(user_router, prefix="/user", tags=["User"])
