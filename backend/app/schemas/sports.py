from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.models.base import DataStatus
from app.models.sports import MatchStatus


class TeamBase(BaseModel):
    id: str
    name: str
    short_name: str
    code: Optional[str] = None
    logo_url: Optional[str] = None
    attack_rating: float = 1.0
    defense_rating: float = 1.0

    model_config = ConfigDict(from_attributes=True)


class PlayerBase(BaseModel):
    id: str
    team_id: str
    name: str
    position: str
    jersey_number: Optional[int] = None
    photo_url: Optional[str] = None
    is_starter: bool = True
    expected_minutes: float = 78.0
    shots_per_90: float = 2.4
    sot_per_90: float = 1.1
    fouls_per_90: float = 1.2
    cards_per_90: float = 0.18
    goals_per_90: float = 0.38
    l5_shots_hit_rate: float = 0.80
    l10_shots_hit_rate: float = 0.75

    model_config = ConfigDict(from_attributes=True)


class OddsItem(BaseModel):
    id: str
    bookmaker: str
    market: str
    selection: str
    line: Optional[float] = None
    odd_value: float
    implied_probability: float
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MatchDetailResponse(BaseModel):
    id: str
    competition_id: str
    competition_name: str
    home_team: TeamBase
    away_team: TeamBase
    match_date: datetime
    status: MatchStatus
    elapsed_minute: int = 0
    home_score: int = 0
    away_score: int = 0
    data_status: DataStatus
    confidence_score: float = 0.95
    source_provider: str
    odds: List[OddsItem] = []

    model_config = ConfigDict(from_attributes=True)


class MarketAnalysisItem(BaseModel):
    market_id: str
    category: str        # GOALS, PLAYER_SHOTS, CORNERS, CARDS
    name: str
    line: Optional[float] = None
    selection: str
    calculated_probability: float
    fair_odds: float
    market_odds: float
    implied_probability: float
    expected_value: float
    confidence_score: float
    risk_level: str      # LOW, MEDIUM, HIGH
    explanation: str
    data_quality: str    # OPTIMAL, SUFFICIENT, LOW
