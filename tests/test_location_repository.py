"""Unit tests for LocationRepository."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from geolibrary.models import Base, Location
from geolibrary.repository import LocationRepository


@pytest.fixture
def test_engine():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_session(test_engine):
    """Create a test database session."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(autouse=True)
def reset_session(test_session: Session):
    """Reset session state before each test."""
    test_session.rollback()
    yield
    test_session.rollback()


@pytest.fixture
def repository(test_session: Session):
    """Create a LocationRepository with a test session."""
    return LocationRepository(session=test_session)


def test_create_and_fetch_location(repository: LocationRepository):
    """Test creating a location and fetching it back with all fields."""
    # Create a location
    location = repository.create_location(
        name="Test Location",
        latitude=40.7128,
        longitude=-74.0060,
        description="A test location in NYC",
    )

    # Verify the created location has correct values
    assert location.id is not None
    assert location.name == "Test Location"
    assert location.latitude == 40.7128
    assert location.longitude == -74.0060
    assert location.description == "A test location in NYC"

    # Fetch the location by ID
    fetched_location = repository.get_location_by_id(location.id)

    # Verify all fields match
    assert fetched_location is not None
    assert fetched_location.id == location.id
    assert fetched_location.name == "Test Location"
    assert fetched_location.latitude == 40.7128
    assert fetched_location.longitude == -74.0060
    assert fetched_location.description == "A test location in NYC"


def test_create_and_fetch_by_name(repository: LocationRepository):
    """Test creating a location and fetching it by name."""
    # Create a location
    location = repository.create_location(
        name="Eiffel Tower",
        latitude=48.8584,
        longitude=2.2945,
        description="Iconic tower in Paris",
    )

    # Fetch by name
    fetched_location = repository.get_location_by_name("Eiffel Tower")

    # Verify all fields
    assert fetched_location is not None
    assert fetched_location.id == location.id
    assert fetched_location.name == "Eiffel Tower"
    assert fetched_location.latitude == 48.8584
    assert fetched_location.longitude == 2.2945
    assert fetched_location.description == "Iconic tower in Paris"


def test_create_location_without_description(repository: LocationRepository):
    """Test creating a location without description."""
    location = repository.create_location(
        name="Simple Location",
        latitude=37.7749,
        longitude=-122.4194,
    )

    # Verify description is None
    assert location.description is None

    # Fetch and verify
    fetched = repository.get_location_by_id(location.id)
    assert fetched is not None
    assert fetched.description is None
    assert fetched.name == "Simple Location"
    assert fetched.latitude == 37.7749
    assert fetched.longitude == -122.4194


def test_create_duplicate_name_raises_error(repository: LocationRepository):
    """Test that creating a location with duplicate name raises ValueError."""
    repository.create_location(
        name="Unique Location",
        latitude=40.0,
        longitude=-70.0,
    )

    # Attempt to create another location with the same name
    with pytest.raises(ValueError, match="already exists"):
        repository.create_location(
            name="Unique Location",
            latitude=50.0,
            longitude=-80.0,
        )

