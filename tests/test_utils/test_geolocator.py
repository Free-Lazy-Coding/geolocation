from app.utils.geolocator import geolocator
from geopy.geocoders import Nominatim


def test_geolocator_initialization():
    assert isinstance(geolocator, Nominatim)
    assert geolocator.headers['User-Agent'] == "geolocation_api"
