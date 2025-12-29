"""Configuration management for geolibrary."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class DatabaseConfig:
    """Database configuration with validation."""

    host: str
    port: int
    user: str
    password: str
    database: str

    def to_url(self) -> str:
        """Convert configuration to SQLAlchemy connection URL."""
        return (
            f"postgresql://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """Load configuration from environment variables."""
        # Try DATABASE_URL first
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            return cls._from_url(database_url)

        # Fallback to individual variables
        host = os.getenv("DB_HOST", "localhost")
        port = int(os.getenv("DB_PORT", "5432"))
        user = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASSWORD", "")
        database = os.getenv("DB_NAME", "geolibrary")

        return cls(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
        )

    @classmethod
    def _from_url(cls, url: str) -> "DatabaseConfig":
        """Parse DATABASE_URL format: postgresql://user:password@host:port/dbname."""
        # Remove postgresql:// prefix
        if url.startswith("postgresql://"):
            url = url[13:]
        elif url.startswith("postgres://"):
            url = url[11:]

        # Split into user:password@host:port/database
        if "@" in url:
            auth_part, location_part = url.split("@", 1)
            if ":" in auth_part:
                user, password = auth_part.split(":", 1)
            else:
                user = auth_part
                password = ""
        else:
            user = "postgres"
            password = ""
            location_part = url

        # Parse host:port/database
        if "/" in location_part:
            host_port, database = location_part.split("/", 1)
        else:
            host_port = location_part
            database = "geolibrary"

        if ":" in host_port:
            host, port_str = host_port.split(":", 1)
            port = int(port_str)
        else:
            host = host_port
            port = 5432

        return cls(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
        )

    @classmethod
    def from_file(cls, file_path: Optional[Path] = None) -> "DatabaseConfig":
        """Load configuration from .env file."""
        if file_path is None:
            file_path = Path.cwd() / ".env"

        if not file_path.exists():
            return cls.from_env()

        # Simple .env file parser
        env_vars: dict[str, str] = {}
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip().strip('"').strip("'")

        # Temporarily set environment variables
        original_env = {}
        for key, value in env_vars.items():
            original_env[key] = os.environ.get(key)
            os.environ[key] = value

        try:
            config = cls.from_env()
        finally:
            # Restore original environment
            for key, original_value in original_env.items():
                if original_value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = original_value

        return config


def get_database_config() -> DatabaseConfig:
    """Get database configuration from file or environment."""
    return DatabaseConfig.from_file()

