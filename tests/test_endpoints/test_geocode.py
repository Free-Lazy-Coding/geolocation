from fastapi import HTTPException

from tests.conftest import sleep


def test_geocode_address_endpoint_successful(test_client, wait_for_rate_limit_reset):
    response = test_client.get(
        "/geocode/",
        params={"q": "New York, NY"},
    )
    assert response.status_code == 200
    assert "latitude" in response.json()
    assert "longitude" in response.json()


def test_geocode_address_endpoint_not_found(test_client, wait_for_rate_limit_reset):
    response = test_client.get(
        "/geocode/",
        params={"q": "Nonexistent City"},
    )
    assert response.status_code == 404
    assert "detail" in response.json()


def test_reverse_geocode_coordinates_endpoint_successful(test_client, wait_for_rate_limit_reset):
    response = test_client.get(
        "/geocode/reverse",
        params={"latitude": 40.7128, "longitude": -74.0060},
    )
    assert response.status_code == 200
    assert "address" in response.json()


def test_geocode_rate_limiting(test_client, wait_for_rate_limit_reset):
    # Send request within the rate limit
    response = test_client.get("/geocode/", params={"q": "London"})
    assert response.status_code == 200

    # Attempt to exceed the rate limit
    response = test_client.get("/geocode/", params={"q": "London"})
    assert response.status_code == 429  # Rate Limit Exceeded
    assert "detail" in response.json()

    # Wait for rate limit to reset
    sleep()
    response = test_client.get("/geocode/", params={"q": "London"})
    assert response.status_code == 200


def test_reverse_geocode_coordinates_endpoint_internal_server_error(
    test_client,
    mock_reverse_geocode_coordinates,
    wait_for_rate_limit_reset,
):
    mock_reverse_geocode_coordinates.side_effect = HTTPException(detail="Geocoding service timed out", status_code=503)
    response = test_client.get(
        "/geocode/reverse",
        params={"latitude": 40.7123, "longitude": -74.0060},
    )
    assert response.status_code == 503
    assert "detail" in response.json()


def test_geocode_address_endpoint_internal_server_error(
    test_client,
    mock_geocode_address,
    wait_for_rate_limit_reset,
):
    mock_geocode_address.side_effect = HTTPException(detail="Geocoding service timed out", status_code=503)
    response = test_client.get(
        "/geocode/",
        params={"q": "New York"},
    )
    assert response.status_code == 503
    assert "detail" in response.json()
