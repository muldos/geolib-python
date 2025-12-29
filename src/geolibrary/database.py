"""Database connection and session management."""

import logging
from sqlalchemy import Engine, create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from geolibrary.config import get_database_config

logger = logging.getLogger(__name__)

_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


def get_engine() -> Engine:
    """Get or create the database engine."""
    global _engine
    if _engine is None:
        config = get_database_config()
        database_url = config.to_url()
        _engine = create_engine(database_url, echo=False)
    return _engine


def get_session() -> sessionmaker[Session]:
    """Get or create the session factory."""
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )
    return _SessionLocal


def create_session() -> Session:
    """Create a new database session."""
    session_factory = get_session()
    return session_factory()


def check_connection() -> bool:
    """Check if database connection is available.

    Returns:
        True if connection is successful, False otherwise
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking database connection: {e}")
        return False


def check_tables_exist(table_names: list[str] | None = None) -> bool:
    """Check if required tables exist in the database.

    Args:
        table_names: List of table names to check. Defaults to ['locations', 'photos']

    Returns:
        True if all tables exist, False otherwise
    """
    if table_names is None:
        table_names = ["locations", "photos"]

    try:
        engine = get_engine()
        inspector = inspect(engine)
        existing_tables = set(inspector.get_table_names())

        missing_tables = [t for t in table_names if t not in existing_tables]
        if missing_tables:
            logger.warning(f"Missing tables: {missing_tables}")
            return False

        return True
    except SQLAlchemyError as e:
        logger.error(f"Error checking tables: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking tables: {e}")
        return False


def get_schema_version() -> str | None:
    """Get the current schema version from the database.

    Returns:
        Schema version string or None if version table doesn't exist
    """
    try:
        engine = get_engine()
        inspector = inspect(engine)

        # Check if schema_version table exists
        if "schema_version" not in inspector.get_table_names():
            return None

        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT version FROM schema_version ORDER BY id DESC LIMIT 1")
            )
            row = result.fetchone()
            return row[0] if row else None
    except SQLAlchemyError as e:
        logger.error(f"Error getting schema version: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error getting schema version: {e}")
        return None


def init_schema_version(version: str) -> bool:
    """Initialize schema version table with the given version.

    Args:
        version: Version string to store

    Returns:
        True if successful, False otherwise
    """
    try:
        engine = get_engine()
        inspector = inspect(engine)

        # Create schema_version table if it doesn't exist
        if "schema_version" not in inspector.get_table_names():
            with engine.begin() as conn:
                conn.execute(
                    text(
                        """
                        CREATE TABLE schema_version (
                            id SERIAL PRIMARY KEY,
                            version VARCHAR(50) NOT NULL,
                            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                        """
                    )
                )

        # Insert version
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO schema_version (version) VALUES (:version)"),
                {"version": version},
            )

        return True
    except SQLAlchemyError as e:
        logger.error(f"Error initializing schema version: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error initializing schema version: {e}")
        return False

