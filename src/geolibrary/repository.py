"""Repository layer with CRUD operations and geospatial logic."""

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import Session

from geolibrary.database import create_session
from geolibrary.models import Location

if TYPE_CHECKING:
    from collections.abc import Sequence


class LocationRepository:
    """Repository for Location CRUD operations and geospatial queries."""

    def __init__(self, session: Session | None = None):
        """Initialize repository with optional session."""
        self._session = session
        self._own_session = session is None

    def __enter__(self):
        """Context manager entry."""
        if self._own_session:
            self._session = create_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self._own_session and self._session:
            if exc_type is None:
                self._session.commit()
            else:
                self._session.rollback()
            self._session.close()

    def _get_session(self) -> Session:
        """Get the current session, creating one if needed."""
        if self._session is None:
            self._session = create_session()
        return self._session

    def create_location(
        self,
        name: str,
        latitude: float,
        longitude: float,
        description: str | None = None,
    ) -> Location:
        """Create a new location.

        Args:
            name: Location name (must be unique)
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            description: Optional description

        Returns:
            Created Location instance

        Raises:
            ValueError: If location with same name already exists
        """
        session = self._get_session()
        # Check if location with same name exists
        stmt = select(Location).where(Location.name == name)
        existing = session.scalar(stmt)
        if existing:
            raise ValueError(f"Location with name '{name}' already exists")

        location = Location(
            name=name,
            description=description,
            latitude=latitude,
            longitude=longitude,
        )
        session.add(location)
        session.commit()
        session.refresh(location)
        return location

    def get_location_by_id(self, location_id: int) -> Location | None:
        """Get location by ID.

        Args:
            location_id: Location ID

        Returns:
            Location instance or None if not found
        """
        session = self._get_session()
        stmt = select(Location).where(Location.id == location_id)
        return session.scalar(stmt)

    def get_location_by_name(self, name: str) -> Location | None:
        """Get location by name.

        Args:
            name: Location name

        Returns:
            Location instance or None if not found
        """
        session = self._get_session()
        stmt = select(Location).where(Location.name == name)
        return session.scalar(stmt)

    def update_location(
        self, location_id: int, **kwargs: str | float | None
    ) -> Location | None:
        """Update location fields.

        Args:
            location_id: Location ID
            **kwargs: Fields to update (name, description, latitude, longitude)

        Returns:
            Updated Location instance or None if not found

        Raises:
            ValueError: If trying to set name to one that already exists
        """
        session = self._get_session()
        location = self.get_location_by_id(location_id)
        if location is None:
            return None

        # Check name uniqueness if name is being updated
        if "name" in kwargs and kwargs["name"] != location.name:
            stmt = select(Location).where(Location.name == kwargs["name"])
            existing = session.scalar(stmt)
            if existing:
                raise ValueError(
                    f"Location with name '{kwargs['name']}' already exists"
                )

        # Update fields
        for key, value in kwargs.items():
            if hasattr(location, key):
                setattr(location, key, value)

        session.commit()
        session.refresh(location)
        return location

    def delete_location(self, location_id: int) -> bool:
        """Delete a location.

        Args:
            location_id: Location ID

        Returns:
            True if deleted, False if not found
        """
        session = self._get_session()
        location = self.get_location_by_id(location_id)
        if location is None:
            return False

        session.delete(location)
        session.commit()
        return True

    def list_locations(self) -> list[Location]:
        """List all locations.

        Returns:
            List of all Location instances
        """
        session = self._get_session()
        stmt = select(Location)
        result = session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    def _is_point_in_polygon(
        point: tuple[float, float], polygon: list[tuple[float, float]]
    ) -> bool:
        """Check if a point is inside a polygon using Ray Casting algorithm.

        Args:
            point: Tuple of (latitude, longitude)
            polygon: List of tuples representing polygon vertices

        Returns:
            True if point is inside polygon, False otherwise
        """
        if len(polygon) < 3:
            return False

        px, py = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            # Skip horizontal edges
            if p1y != p2y:
                # Check if ray intersects with this edge
                if py > min(p1y, p2y) and py <= max(p1y, p2y):
                    if px <= max(p1x, p2x):
                        # Calculate x-coordinate of intersection
                        if p1x == p2x:
                            # Vertical edge
                            inside = not inside
                        else:
                            xinters = (py - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if px <= xinters:
                                inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def get_locations_in_perimeter(
        self, polygon_points: list[tuple[float, float]]
    ) -> list[Location]:
        """Get all locations within a polygon perimeter.

        Args:
            polygon_points: List of (latitude, longitude) tuples forming polygon

        Returns:
            List of Location instances within the polygon
        """
        session = self._get_session()
        stmt = select(Location)
        result = session.execute(stmt)
        all_locations = list(result.scalars().all())

        filtered_locations = [
            loc
            for loc in all_locations
            if self._is_point_in_polygon(
                (loc.latitude, loc.longitude), polygon_points
            )
        ]

        return filtered_locations

