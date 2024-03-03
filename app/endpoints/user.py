from typing import Annotated

from fastapi import APIRouter, Depends, Request
from app.services.user import get_user_ip, get_lat_lon
from app.models import IPRequest, IPResponse, ErrorResponse, CoordinatesResponse
from app.utils.cache import cache_response

router = APIRouter()


@router.get(
    "/ip",
    summary="Get user's IP address",
    response_model=IPResponse,
    responses={
        404: {
            "model": ErrorResponse,
        },
    },
)
@cache_response()
async def get_user_ip_endpoint(request: Request):
    """
    Get the user's IP address.

    Returns:
    - IPResponse: Response model containing the user's IP address.
    """
    return await get_user_ip(request)


@router.get(
    "/ip/{ip_address}",
    summary="Get latitude and longitude coordinates from IP address",
    response_model=CoordinatesResponse,
    responses={
        404: {
            "model": ErrorResponse,
        },
    },
)
@cache_response()
async def get_lat_lon_endpoint(request:  Annotated[IPRequest, Depends()]):
    """
    Get latitude and longitude coordinates corresponding to the provided IP address.

    Args:
    - request (IPRequest): Request model containing the IP address.

    Returns:
    - CoordinatesResponse: Response model containing the latitude and longitude coordinates.
    """
    return await get_lat_lon(request.ip_address)
