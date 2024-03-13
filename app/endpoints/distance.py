from typing import Annotated

from fastapi import APIRouter, Depends

from app.services.distance import get_distance, calculate_distance
from app.models import DistanceRequest, CoordinatesRequest, DistanceResponse, ErrorResponse
from app.utils.cache import cache_response

router = APIRouter()


@router.get(
    "/addresses",
    summary="Calculate distance between two addresses",
    response_model=DistanceResponse,
    responses={
        503: {
            "model": ErrorResponse,
        },
    },
)
@cache_response()
async def get_distance_endpoint(request: Annotated[DistanceRequest, Depends()]):
    """
    Calculate the distance in kilometers between two addresses.

    Args:
    - request (DistanceRequest): Request model containing two addresses.

    Returns:
    - DistanceResponse: Response model containing the calculated distance.
    """
    return await get_distance(request.address1, request.address2)


@router.get(
    "/coordinates",
    summary="Calculate distance between two sets of coordinates",
    response_model=DistanceResponse,
    responses={
        404: {
            "model": ErrorResponse,
        },
        503: {
            "model": ErrorResponse,
        },
    },
)
@cache_response()
async def calculate_distance_endpoint(request: Annotated[CoordinatesRequest, Depends()]):
    """
    Calculate the distance in kilometers between two sets of coordinates.

    Args:
    - request (CoordinatesRequest): Request model containing latitude and longitude coordinates.

    Returns:
    - DistanceResponse: Response model containing the calculated distance.
    """
    return await calculate_distance(request.lat1, request.lon1, request.lat2, request.lon2)
