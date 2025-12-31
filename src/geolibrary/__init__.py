"""Geolibrary - A modern Python library for geospatial location management."""

from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
import tomllib

try:
    __version__ = version("geolibrary")
except PackageNotFoundError:
    # Package is not installed, read from pyproject.toml during development
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    if pyproject_path.exists():
        with open(pyproject_path, "rb") as f:
            __version__ = tomllib.load(f)["tool"]["poetry"]["version"]
    else:
        __version__ = "0.0.0"

from geolibrary.database import (
    check_connection,
    check_tables_exist,
    create_session,
    get_engine,
    get_session,
)
from geolibrary.models import Location, Photo
from geolibrary.repository import LocationRepository
from geolibrary.version import DATAMODEL_VERSION

__all__ = [
    "Location",
    "Photo",
    "LocationRepository",
    "get_engine",
    "get_session",
    "create_session",
    "check_connection",
    "check_tables_exist",
    "DATAMODEL_VERSION",
]

