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
    """Get or create the database engine.
    
    Configures connection pool with:
    - pool_size: Number of connections to maintain (default: 5)
    - max_overflow: Additional connections beyond pool_size (default: 10)
    - pool_pre_ping: Test connections before using (prevents stale connections)
    - pool_recycle: Recycle connections after this many seconds (default: 3600)
    - pool_timeout: Seconds to wait for connection from pool (default: 30)
    """
    global _engine
    if _engine is None:
        config = get_database_config()
        database_url = config.to_url()
        
        # Configure connection pool settings
        # Both schemas (public and geoiam) share the same pool since they're in the same database
        _engine = create_engine(
            database_url,
            echo=False,
            pool_size=5,  # Number of connections to maintain
            max_overflow=10,  # Additional connections beyond pool_size
            pool_pre_ping=True,  # Test connections before using (prevents stale connections)
            pool_recycle=3600,  # Recycle connections after 1 hour
            pool_timeout=30,  # Wait up to 30 seconds for a connection from the pool
            connect_args={
                "connect_timeout": 10,  # Connection timeout in seconds
            }
        )
        logger.info(
            f"Database engine created with pool_size=5, max_overflow=10, "
            f"pool_pre_ping=True, pool_recycle=3600"
        )
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

