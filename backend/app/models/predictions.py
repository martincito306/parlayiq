import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean, Enum, JSON
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base
from app.models.base import MetadataMixin


class PredictionStatus(str, enum.Enum):
    PENDING = "PENDING"
    WON = "WON"
    LOST = "LOST"
    VOID = "VOID"


class RiskTier(str, enum.Enum):
    CONSERVATIVE = "CONSERVATIVE"
    BALANCED = "BALANCED"
    HIGH_YIELD = "HIGH_YIELD"


class Prediction(Base, MetadataMixin):
    __tablename__ = "predictions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    match_id = Column(String(36), ForeignKey("matches.id"), nullable=False)
    player_id = Column(String(36), ForeignKey("players.id"), nullable=True)
    
    market = Column(String(50), nullable=False)      # e.g., OVER_UNDER_GOALS, BOTH_TEAMS_TO_SCORE, PLAYER_SHOTS_ON_TARGET
    selection = Column(String(50), nullable=False)   # e.g., "OVER_2.5", "YES", "OVER_1.5"
    line = Column(Float, nullable=True)
    
    # Quantitative evaluation
    calculated_probability = Column(Float, nullable=False)
    fair_odds = Column(Float, nullable=False)
    market_odds = Column(Float, nullable=False)
    implied_probability = Column(Float, nullable=False)
    expected_value = Column(Float, nullable=False)  # EV = (P * odds) - 1
    
    model_name = Column(String(50), default="DIXON_COLES_V1", nullable=False)
    model_version = Column(String(20), default="1.0.0", nullable=False)
    confidence_level = Column(String(20), default="HIGH", nullable=False) # LOW, MEDIUM, HIGH
    
    # Audit & settlement
    status = Column(Enum(PredictionStatus), default=PredictionStatus.PENDING, nullable=False, index=True)
    actual_result = Column(String(50), nullable=True)
    brier_score = Column(Float, nullable=True)
    settled_at = Column(DateTime, nullable=True)

    match = relationship("Match")
    player = relationship("Player")


class Parlay(Base, MetadataMixin):
    __tablename__ = "parlays"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    title = Column(String(100), default="Combinada Inteligente", nullable=False)
    risk_tier = Column(Enum(RiskTier), default=RiskTier.BALANCED, nullable=False)
    
    joint_probability = Column(Float, nullable=False)
    fair_odds = Column(Float, nullable=False)
    market_odds = Column(Float, nullable=False)
    expected_value = Column(Float, nullable=False)
    
    monte_carlo_iterations = Column(Integer, default=10000, nullable=False)
    correlation_penalty = Column(Float, default=0.0) # difference between independent and copula joint prob
    
    explanation = Column(String(1000), nullable=True)
    status = Column(Enum(PredictionStatus), default=PredictionStatus.PENDING, nullable=False)

    legs = relationship("ParlayLeg", back_populates="parlay", cascade="all, delete-orphan")


class ParlayLeg(Base, MetadataMixin):
    __tablename__ = "parlay_legs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    parlay_id = Column(String(36), ForeignKey("parlays.id"), nullable=False)
    match_id = Column(String(36), ForeignKey("matches.id"), nullable=False)
    player_id = Column(String(36), ForeignKey("players.id"), nullable=True)
    
    market = Column(String(50), nullable=False)
    selection = Column(String(50), nullable=False)
    line = Column(Float, nullable=True)
    individual_probability = Column(Float, nullable=False)
    individual_odds = Column(Float, nullable=False)
    ev = Column(Float, nullable=False)
    
    # Diagnostic alert from Smart Slip Auditor
    is_weak_leg = Column(Boolean, default=False)
    weak_reason = Column(String(255), nullable=True)
    status = Column(Enum(PredictionStatus), default=PredictionStatus.PENDING, nullable=False)

    parlay = relationship("Parlay", back_populates="legs")
    match = relationship("Match")
    player = relationship("Player")


class ModelPerformanceRecord(Base, MetadataMixin):
    __tablename__ = "model_performance_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    model_name = Column(String(50), nullable=False)
    market = Column(String(50), default="ALL", nullable=False)
    
    total_predictions = Column(Integer, default=0, nullable=False)
    won_predictions = Column(Integer, default=0, nullable=False)
    lost_predictions = Column(Integer, default=0, nullable=False)
    win_rate = Column(Float, default=0.0, nullable=False)
    
    brier_score = Column(Float, default=0.0, nullable=False)
    expected_calibration_error = Column(Float, default=0.0, nullable=False)
    simulated_roi = Column(Float, default=0.0, nullable=False) # e.g. +14.2%
    closing_line_value_avg = Column(Float, default=0.0)
