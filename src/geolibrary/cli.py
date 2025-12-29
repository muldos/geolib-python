"""Command-line interface for geolibrary."""

import sys
from typing import Optional

import click

from geolibrary.database import get_engine
from geolibrary.models import Base, Location
from geolibrary.repository import LocationRepository


@click.group()
@click.version_option(version="0.1.0")
def main() -> None:
    """Geolibrary CLI - Manage geospatial locations."""
    pass


@main.command()
def init_db() -> None:
    """Initialize the database tables."""
    try:
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
        click.echo("Database initialized successfully.")
    except Exception as e:
        click.echo(f"Error initializing database: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--name", required=True, help="Location name")
@click.option("--description", help="Location description")
@click.option(
    "--latitude",
    required=True,
    type=float,
    help="Latitude coordinate",
)
@click.option(
    "--longitude",
    required=True,
    type=float,
    help="Longitude coordinate",
)
def add(name: str, description: Optional[str], latitude: float, longitude: float) -> None:
    """Add a new location."""
    try:
        with LocationRepository() as repo:
            location = repo.create_location(
                name=name,
                description=description,
                latitude=latitude,
                longitude=longitude,
            )
            click.echo(f"Location created: {location}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


@main.command(name="list")
def list_locations() -> None:
    """List all locations."""
    try:
        with LocationRepository() as repo:
            locations = repo.list_locations()
            if not locations:
                click.echo("No locations found.")
                return

            click.echo(f"Found {len(locations)} location(s):\n")
            for loc in locations:
                click.echo(
                    f"ID: {loc.id} | Name: {loc.name} | "
                    f"Lat: {loc.latitude}, Lon: {loc.longitude}"
                )
                if loc.description:
                    click.echo(f"  Description: {loc.description}")
                click.echo()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--id", "location_id", type=int, help="Location ID")
@click.option("--name", help="Location name")
def get(location_id: Optional[int], name: Optional[str]) -> None:
    """Get a location by ID or name."""
    if not location_id and not name:
        click.echo("Error: Must provide either --id or --name", err=True)
        sys.exit(1)

    if location_id and name:
        click.echo("Error: Provide either --id or --name, not both", err=True)
        sys.exit(1)

    try:
        with LocationRepository() as repo:
            if location_id:
                location = repo.get_location_by_id(location_id)
            else:
                location = repo.get_location_by_name(name)  # type: ignore

            if location is None:
                click.echo("Location not found.", err=True)
                sys.exit(1)

            click.echo(f"Location found:")
            click.echo(f"  ID: {location.id}")
            click.echo(f"  Name: {location.name}")
            click.echo(f"  Latitude: {location.latitude}")
            click.echo(f"  Longitude: {location.longitude}")
            if location.description:
                click.echo(f"  Description: {location.description}")
            if location.photos:
                click.echo(f"  Photos: {len(location.photos)}")
                for photo in location.photos:
                    click.echo(f"    - {photo.filename}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("points", required=True)
def search_area(points: str) -> None:
    """Search locations within a polygon area.

    POINTS: Space-separated coordinate pairs in 'lat,lon' format
    Example: "40.7,-74.0 40.8,-74.0 40.8,-73.9 40.7,-73.9"
    """
    try:
        # Parse points string
        point_strings = points.strip().split()
        if len(point_strings) < 3:
            click.echo(
                "Error: Polygon must have at least 3 points", err=True
            )
            sys.exit(1)

        polygon_points: list[tuple[float, float]] = []
        for point_str in point_strings:
            try:
                parts = point_str.split(",")
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())
                polygon_points.append((lat, lon))
            except (ValueError, IndexError) as e:
                click.echo(
                    f"Error: Invalid point format '{point_str}'. "
                    f"Expected 'lat,lon'",
                    err=True,
                )
                sys.exit(1)

        with LocationRepository() as repo:
            locations = repo.get_locations_in_perimeter(polygon_points)

            if not locations:
                click.echo(
                    f"No locations found within the specified polygon area."
                )
                return

            click.echo(
                f"Found {len(locations)} location(s) within polygon:\n"
            )
            for loc in locations:
                click.echo(
                    f"ID: {loc.id} | Name: {loc.name} | "
                    f"Lat: {loc.latitude}, Lon: {loc.longitude}"
                )
                if loc.description:
                    click.echo(f"  Description: {loc.description}")
                click.echo()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

