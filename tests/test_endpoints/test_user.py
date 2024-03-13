from tests.conftest import sleep


def test_get_user_ip_endpoint_successful(test_client, wait_for_rate_limit_reset):
    response = test_client.get("/user/ip")
    assert response.status_code == 200
    assert "ip" in response.json()


def test_get_user_ip_endpoint_rate_limiting(test_client, wait_for_rate_limit_reset):
    # Send request within the rate limit
    response = test_client.get("/user/ip")
    assert response.status_code == 200

    # Attempt to exceed the rate limit
    response = test_client.get("/user/ip")
    assert response.status_code == 429  # Rate Limit Exceeded
    assert "detail" in response.json()

    # Wait for rate limit to reset
    sleep()

    # Send request within the rate limit again
    response = test_client.get("/user/ip")
    assert response.status_code == 200


def test_get_lat_lon_endpoint_successful(test_client, wait_for_rate_limit_reset):
    response = test_client.get("/user/ip/8.8.8.8")
    assert response.status_code == 200
    assert "latitude" in response.json()
    assert "longitude" in response.json()


def test_get_lat_lon_endpoint_not_found(test_client, wait_for_rate_limit_reset):
    response = test_client.get("/user/ip/invalid_ip")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_lat_lon_endpoint_rate_limiting(test_client, wait_for_rate_limit_reset):
    # Send request within the rate limit
    response = test_client.get("/user/ip/8.8.8.8")
    assert response.status_code == 200

    # Attempt to exceed the rate limit
    response = test_client.get("/user/ip/8.8.8.8")
    assert response.status_code == 429  # Rate Limit Exceeded
    assert "detail" in response.json()

    # Wait for rate limit to reset
    sleep()

    # Send request within the rate limit again
    response = test_client.get("/user/ip/8.8.8.8")
    assert response.status_code == 200
