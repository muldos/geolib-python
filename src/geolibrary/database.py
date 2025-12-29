"""Database connection and session management."""

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from geolibrary.config import get_database_config

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

