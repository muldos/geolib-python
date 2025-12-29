"""SQLAlchemy 2.0 data models."""

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from collections.abc import Sequence


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class Location(Base):
    """Location model representing a geographic location."""

    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    photos: Mapped[list["Photo"]] = relationship(
        "Photo", back_populates="location", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation of Location."""
        return (
            f"<Location(id={self.id}, name='{self.name}', "
            f"lat={self.latitude}, lon={self.longitude})>"
        )


class Photo(Base):
    """Photo model representing a photo associated with a location."""

    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(512), nullable=False)
    location_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("locations.id"), nullable=False
    )

    location: Mapped["Location"] = relationship("Location", back_populates="photos")

    def __repr__(self) -> str:
        """String representation of Photo."""
        return f"<Photo(id={self.id}, filename='{self.filename}', location_id={self.location_id})>"

