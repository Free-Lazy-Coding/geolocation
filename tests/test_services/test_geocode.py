from fastapi import HTTPException
import pytest

from app.services.geocode import geocode_address, reverse_geocode_coordinates


@pytest.mark.asyncio
async def test_geocode_address_successful(mock_services_geocode):
    mock_services_geocode.return_value.latitude = 40.7128
    mock_services_geocode.return_value.longitude = -74.0060

    result = await geocode_address("New York, NY")

    assert result == {"latitude": 40.7128, "longitude": -74.0060}


@pytest.mark.asyncio
async def test_geocode_address_not_found(mock_services_geocode):
    mock_services_geocode.return_value = None  # Simulate location not found

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
