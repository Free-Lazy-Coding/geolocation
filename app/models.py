from pydantic import BaseModel


class GeocodeRequest(BaseModel):
    q: str


class GeocodeResponse(BaseModel):
    latitude: float
    longitude: float


class ReverseGeocodeRequest(BaseModel):
    latitude: float
    longitude: float


class ReverseGeocodeResponse(BaseModel):
    address: str


class DistanceRequest(BaseModel):
    address1: str
    address2: str


class DistanceResponse(BaseModel):
    distance: float


class CoordinatesRequest(BaseModel):
    lat1: float
    lon1: float
    lat2: float
    lon2: float


class CoordinatesResponse(BaseModel):
    latitude: float
    longitude: float


class IPRequest(BaseModel):
    ip_address: str


class IPResponse(BaseModel):
    ip: str


class ErrorResponse(BaseModel):
    detail: str
