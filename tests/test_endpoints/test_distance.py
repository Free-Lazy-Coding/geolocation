from fastapi import HTTPException


def test_get_distance_endpoint_successful(test_client, wait_for_rate_limit_reset):
    response = test_client.get(
        "/distance/addresses",
        params={"address1": "New York, NY", "address2": "Los Angeles, CA"},
    )
    assert response.status_code == 200
    assert "distance" in response.json()


def test_get_distance_endpoint_address_not_found(test_client, wait_for_rate_limit_reset):
    response = test_client.get(
        "/distance/addresses",
        params={"address1": "Nonexistent City", "address2": "Another Nonexistent City"},
    )
    assert response.status_code == 404
    assert "detail" in response.json()


def test_calculate_distance_endpoint_successful(test_client, wait_for_rate_limit_reset):
    response = test_client.get(
        "/distance/coordinates",
        params={"lat1": 40.7128, "lon1": -74.0060, "lat2": 34.0522, "lon2": -118.2437},
    )
    assert response.status_code == 200
    assert "distance" in response.json()


def test_rate_limiting(test_client, wait_for_rate_limit_reset):
    # Send request within the rate limit
    response = test_client.get("/distance/addresses", params={"address1": "London", "address2": "Paris"})
    assert response.status_code == 200

    # Attempt to exceed the rate limit
    response = test_client.get("/distance/addresses", params={"address1": "London", "address2": "Paris"})
    assert response.status_code == 429  # Rate Limit Exceeded
    assert "detail" in response.json()


def test_calculate_distance_endpoint_internal_server_error(
    test_client,
    mock_calculate_distance,
    wait_for_rate_limit_reset,
):
    mock_calculate_distance.side_effect = HTTPException(detail="Geocoding service timed out", status_code=503)
    response = test_client.get(
        "/distance/coordinates",
        params={"lat1": 40.7120, "lon1": -74.0060, "lat2": 34.0522, "lon2": -118.2437},
    )
    assert response.status_code == 503
    assert "detail" in response.json()


def test_get_distance_endpoint_internal_server_error(
    test_client,
    mock_get_distance,
    wait_for_rate_limit_reset,
):
    mock_get_distance.side_effect = HTTPException(detail="Geocoding service timed out", status_code=503)
    response = test_client.get(
        "/distance/addresses",
        params={"address1": "Milan", "address2": "Paris"},
    )
    assert response.status_code == 503
    assert "detail" in response.json()
