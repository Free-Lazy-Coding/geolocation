from fastapi import HTTPException
import pytest
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut

from app.services.geocode import geocode_address, reverse_geocode_coordinates


@pytest.mark.asyncio
async def test_geocode_address_successful(mock_geocode):
    mock_geocode.return_value.latitude = 40.7128
    mock_geocode.return_value.longitude = -74.0060

    result = await geocode_address("New York, NY")

    assert result == {"latitude": 40.7128, "longitude": -74.0060}


@pytest.mark.asyncio
async def test_geocode_address_not_found(mock_geocode):
    mock_geocode.return_value = None  # Simulate location not found

    with pytest.raises(HTTPException) as exc_info:
        await geocode_address("Nonexistent City")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Location not found"


@pytest.mark.asyncio
async def test_reverse_geocode_coordinates_successful(mock_reverse):
    mock_reverse.return_value.address = "New York, NY, USA"

    result = await reverse_geocode_coordinates(40.7128, -74.0060)

    assert result == {"address": "New York, NY, USA"}


@pytest.mark.asyncio
async def test_reverse_geocode_coordinates_not_found(mock_reverse):
    mock_reverse.return_value = None  # Simulate address not found

    with pytest.raises(HTTPException) as exc_info:
        await reverse_geocode_coordinates(40.7128, -74.0060)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Address not found"


@pytest.mark.asyncio
async def test_geocode_address_geocoder_timed_out(mock_geocode):
    mock_geocode.side_effect = GeocoderTimedOut()

    with pytest.raises(HTTPException) as exc_info:
        await geocode_address("New York, NY")

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Geocoding service timed out"


@pytest.mark.asyncio
async def test_geocode_address_geocoder_unavailable(mock_geocode):
    mock_geocode.side_effect = GeocoderUnavailable()

    with pytest.raises(HTTPException) as exc_info:
        await geocode_address("New York, NY")

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Geocoding service timed out"


@pytest.mark.asyncio
async def test_reverse_geocode_coordinates_geocoder_timed_out(mock_reverse):
    mock_reverse.side_effect = GeocoderTimedOut()

    with pytest.raises(HTTPException) as exc_info:
        await reverse_geocode_coordinates(40.7128, -74.0060)

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Geocoding service timed out"


@pytest.mark.asyncio
async def test_reverse_geocode_coordinates_geocoder_unavailable(mock_reverse):
    mock_reverse.side_effect = GeocoderUnavailable()

    with pytest.raises(HTTPException) as exc_info:
        await reverse_geocode_coordinates(40.7128, -74.0060)

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Geocoding service timed out"
