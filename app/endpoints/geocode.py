from typing import Annotated

from fastapi import APIRouter, Depends
from app.services.geocode import geocode_address, reverse_geocode_coordinates
from app.models import GeocodeRequest, ReverseGeocodeRequest, GeocodeResponse, ReverseGeocodeResponse, ErrorResponse
from app.utils.cache import cache_response

router = APIRouter()


@router.get(
    "/",
    summary="Geocode an address",
    response_model=GeocodeResponse,
    responses={
        404: {
            "model": ErrorResponse,
        },
    },
)
@cache_response()
async def geocode_address_endpoint(request: Annotated[GeocodeRequest, Depends()]):
    """
    Geocode an address to obtain its latitude and longitude coordinates.

    Args:
    - request (GeocodeRequest): Request model containing the address to geocode.

    Returns:
    - GeocodeResponse: Response model containing the latitude and longitude coordinates.
    """
    return await geocode_address(request.q)


@router.get(
    "/reverse",
    summary="Reverse geocode coordinates",
    response_model=ReverseGeocodeResponse,
    responses={
        404: {
            "model": ErrorResponse,
        },
    },
)
@cache_response()
async def reverse_geocode_coordinates_endpoint(request: Annotated[ReverseGeocodeRequest, Depends()]):
    """
    Reverse geocode latitude and longitude coordinates to obtain the corresponding address.

    Args:
    - request (ReverseGeocodeRequest): Request model containing latitude and longitude coordinates.

    Returns:
    - ReverseGeocodeResponse: Response model containing the corresponding address.
    """
    return await reverse_geocode_coordinates(request.latitude, request.longitude)
