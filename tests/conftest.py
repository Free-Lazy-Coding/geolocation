import time
import warnings

import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from unittest import mock


@pytest.fixture(autouse=True)
def ignore_warnings():
    warnings.filterwarnings("ignore")


@pytest.fixture
def mock_redis():
    with mock.patch("app.utils.cache.redis_connection") as mock_redis:
        yield mock_redis


@pytest.fixture
def mock_geocode():
    with mock.patch("app.services.distance.geolocator.geocode") as mock_geocode:
        yield mock_geocode


@pytest.fixture
def mock_geodesic():
    with mock.patch("app.services.distance.geodesic") as mock_geodesic:
        yield mock_geodesic


@pytest.fixture
def mock_reverse():
    with mock.patch("app.services.geocode.geolocator.reverse") as mock_reverse:
        yield mock_reverse


@pytest.fixture
def mock_request():
    request = mock.Mock(spec=Request)
    request.client.host = "127.0.0.1"
    request.headers = {"X-Forwarded-For": request.client.host}
    return request


@pytest.fixture
def mock_httpx_get():
    with mock.patch("httpx.AsyncClient.get") as mock_httpx_get:
        yield mock_httpx_get


@pytest.fixture
def mock_calculate_distance():
    with mock.patch("app.endpoints.distance.calculate_distance") as mock_calculate_distance:
        yield mock_calculate_distance


@pytest.fixture
def mock_reverse_geocode_coordinates():
    with mock.patch("app.endpoints.geocode.reverse_geocode_coordinates") as mock_reverse_geocode_coordinates:
        yield mock_reverse_geocode_coordinates


@pytest.fixture
def mock_geocode_address():
    with mock.patch("app.endpoints.geocode.geocode_address") as mock_geocode_address:
        yield mock_geocode_address


@pytest.fixture
def mock_get_distance():
    with mock.patch("app.endpoints.distance.get_distance") as mock_get_distance:
        yield mock_get_distance


@pytest.fixture
def wait_for_rate_limit_reset():
    sleep()


def sleep():
    time.sleep(3)


@pytest.fixture
def test_client():
    from app.main import app
    from app.utils.cache import redis_connection

    # Use the TestClient with a test database
    with TestClient(app, headers={"X-Forwarded-For": "127.0.0.1"}) as client:
        yield client
