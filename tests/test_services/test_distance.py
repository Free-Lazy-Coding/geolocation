import pytest
from fastapi import HTTPException
from unittest import mock

from geopy.exc import GeocoderUnavailable, GeocoderTimedOut

from app.services.distance import get_distance, calculate_distance


@pytest.mark.asyncio
async def test_get_distance_successful(mock_geocode):
    mock_geocode.side_effect = [
        mock.AsyncMock(latitude=40.7128, longitude=-74.0060),  # New York
        mock.AsyncMock(latitude=34.0522, longitude=-118.2437),  # Los Angeles
    ]

    result = await get_distance("New York, NY", "Los Angeles, CA")

    assert result == {"distance": 3944.422231489921}  # Approximate distance in kilometers


@pytest.mark.asyncio
async def test_get_distance_address_not_found(mock_geocode):
    mock_geocode.return_value = None  # Simulate address not found

    with pytest.raises(HTTPException) as exc_info:
        await get_distance("Nonexistent City", "Another Nonexistent City")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "One or both addresses not found"


@pytest.mark.asyncio
async def test_calculate_distance():
    result = await calculate_distance(40.7128, -74.0060, 34.0522, -118.2437)

    assert result == {"distance": 3944.422231489921}  # Approximate distance in kilometers


@pytest.mark.asyncio
async def test_get_distance_geocoder_timed_out(mock_geocode):
    mock_geocode.side_effect = GeocoderTimedOut()
    with pytest.raises(HTTPException) as exc_info:
        await get_distance("New York, NY", "Los Angeles, CA")
    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Geocoding service timed out"


@pytest.mark.asyncio
async def test_get_distance_geocoder_unavailable(mock_geocode):
    mock_geocode.side_effect = GeocoderUnavailable()
    with pytest.raises(HTTPException) as exc_info:
        await get_distance("New York, NY", "Los Angeles, CA")
    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Geocoding service timed out"


@pytest.mark.asyncio
async def test_calculate_distance_geocoder_timed_out(mock_geodesic):
    mock_geodesic.side_effect = GeocoderTimedOut()
    with pytest.raises(HTTPException) as exc_info:
        await calculate_distance(40.7128, -74.0060, 34.0522, -118.2437)
    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Geocoding service timed out"


@pytest.mark.asyncio
async def test_calculate_distance_geocoder_unavailable(mock_geodesic):
    mock_geodesic.side_effect = GeocoderUnavailable()
    with pytest.raises(HTTPException) as exc_info:
        await calculate_distance(40.7128, -74.0060, 34.0522, -118.2437)
    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Geocoding service timed out"
