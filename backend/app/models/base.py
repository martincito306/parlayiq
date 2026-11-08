import enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float, Enum
from app.core.database import Base


class DataStatus(str, enum.Enum):
    LIVE = "LIVE"
    CONFIRMED = "CONFIRMED"
    PROVISIONAL = "PROVISIONAL"
    PROVISIONAL_SYNTHETIC = "PROVISIONAL_SYNTHETIC"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"


class MetadataMixin:
    """Standard tracking metadata required by PARLAYIQ for all sport entities."""
    source_provider = Column(String(50), default="football-data.co.uk", nullable=False)
    data_status = Column(Enum(DataStatus), default=DataStatus.CONFIRMED, nullable=False)
    confidence_score = Column(Float, default=1.0, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
