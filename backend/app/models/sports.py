import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base
from app.models.base import MetadataMixin, DataStatus


class MatchStatus(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    IN_PLAY = "IN_PLAY"
    FINISHED = "FINISHED"
    POSTPONED = "POSTPONED"
    CANCELLED = "CANCELLED"


class Competition(Base, MetadataMixin):
    __tablename__ = "competitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    country = Column(String(50), nullable=False)
    code = Column(String(20), unique=True, index=True, nullable=False)  # e.g., 'PL', 'PD', 'SA', 'BL1'
    season = Column(String(20), default="2025/2026", nullable=False)
    logo_url = Column(String(255), nullable=True)

    matches = relationship("Match", back_populates="competition")


class Team(Base, MetadataMixin):
    __tablename__ = "teams"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    short_name = Column(String(50), nullable=False)
    code = Column(String(10), nullable=True)
    logo_url = Column(String(255), nullable=True)
    venue = Column(String(100), nullable=True)
    
    # Quantitative parameters
    attack_rating = Column(Float, default=1.0)
    defense_rating = Column(Float, default=1.0)

    players = relationship("Player", back_populates="team")


class Player(Base, MetadataMixin):
    __tablename__ = "players"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = Column(String(36), ForeignKey("teams.id"), nullable=False)
    name = Column(String(100), nullable=False)
    position = Column(String(20), default="FWD", nullable=False)  # GK, DEF, MID, FWD
    jersey_number = Column(Integer, nullable=True)
    photo_url = Column(String(255), nullable=True)
    is_starter = Column(Boolean, default=True)
    expected_minutes = Column(Float, default=78.0)
    
    # Season per-90 metrics
    shots_per_90 = Column(Float, default=2.4)
    sot_per_90 = Column(Float, default=1.1)  # Shots on Target
    fouls_per_90 = Column(Float, default=1.2)
    cards_per_90 = Column(Float, default=0.18)
    goals_per_90 = Column(Float, default=0.38)
    
    # L5 & L10 hit rates for over 1.5 shots / 0.5 SOT
    l5_shots_hit_rate = Column(Float, default=0.80)  # 80%
    l10_shots_hit_rate = Column(Float, default=0.75) # 75%

    team = relationship("Team", back_populates="players")
    statistics = relationship("PlayerStatistic", back_populates="player")


class Match(Base, MetadataMixin):
    __tablename__ = "matches"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    competition_id = Column(String(36), ForeignKey("competitions.id"), nullable=False)
    home_team_id = Column(String(36), ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(String(36), ForeignKey("teams.id"), nullable=False)
    
    match_date = Column(DateTime, nullable=False, index=True)
    status = Column(Enum(MatchStatus), default=MatchStatus.SCHEDULED, nullable=False, index=True)
    elapsed_minute = Column(Integer, default=0)
    
    # Scores
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    half_time_home = Column(Integer, default=0)
    half_time_away = Column(Integer, default=0)

    competition = relationship("Competition", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])
    odds = relationship("Odds", back_populates="match")
    match_statistics = relationship("MatchStatistic", back_populates="match")
    player_statistics = relationship("PlayerStatistic", back_populates="match")


class MatchStatistic(Base, MetadataMixin):
    __tablename__ = "match_statistics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    match_id = Column(String(36), ForeignKey("matches.id"), nullable=False)
    team_id = Column(String(36), ForeignKey("teams.id"), nullable=False)
    
    shots = Column(Integer, default=0)
    shots_on_target = Column(Integer, default=0)
    corners = Column(Integer, default=0)
    fouls = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    possession_pct = Column(Float, default=50.0)
    xg = Column(Float, default=1.35)

    match = relationship("Match", back_populates="match_statistics")


class PlayerStatistic(Base, MetadataMixin):
    __tablename__ = "player_statistics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    player_id = Column(String(36), ForeignKey("players.id"), nullable=False)
    match_id = Column(String(36), ForeignKey("matches.id"), nullable=False)
    
    minutes_played = Column(Integer, default=90)
    shots = Column(Integer, default=0)
    shots_on_target = Column(Integer, default=0)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    fouls_committed = Column(Integer, default=0)
    fouls_drawn = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    rating = Column(Float, default=7.0)

    player = relationship("Player", back_populates="statistics")
    match = relationship("Match", back_populates="player_statistics")


class Odds(Base, MetadataMixin):
    __tablename__ = "odds"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    match_id = Column(String(36), ForeignKey("matches.id"), nullable=False)
    bookmaker = Column(String(50), default="Pinnacle", nullable=False)
    market = Column(String(50), nullable=False)  # 1X2, OVER_UNDER, BTTS, CORNERS, CARDS, PLAYER_SHOTS
    selection = Column(String(50), nullable=False) # e.g. "HOME", "OVER_2.5", "YES", "OVER_1.5_SOT"
    line = Column(Float, nullable=True)
    odd_value = Column(Float, nullable=False)
    implied_probability = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    match = relationship("Match", back_populates="odds")
