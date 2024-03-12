import warnings

import pytest
from unittest import mock


@pytest.fixture(autouse=True)
def ignore_deprecation_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.fixture
def mock_redis():
    with mock.patch("app.utils.cache.redis_connection") as mock_redis:
        yield mock_redis


@pytest.fixture
def mock_geocode():
    with mock.patch("app.services.distance.geolocator.geocode") as mock_geocode:
        yield mock_geocode


@pytest.fixture
def mock_services_geocode():
    with mock.patch("app.services.geocode.geolocator.geocode") as mock_geocode:
        yield mock_geocode


@pytest.fixture
def mock_reverse():
    with mock.patch("app.services.geocode.geolocator.reverse") as mock_reverse:
        yield mock_reverse
