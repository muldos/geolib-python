"""Geolibrary - A modern Python library for geospatial location management."""

__version__ = "0.1.0"

from geolibrary.database import get_engine, get_session
from geolibrary.models import Location, Photo
from geolibrary.repository import LocationRepository

__all__ = [
    "Location",
    "Photo",
    "LocationRepository",
    "get_engine",
    "get_session",
]

