from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.predictions import RiskTier, PredictionStatus


class ParlayLegInput(BaseModel):
    match_id: str
    player_id: Optional[str] = None
    market: str
    selection: str
    line: Optional[float] = None
    market_odds: float = Field(..., gt=1.0)
    label: Optional[str] = None


class ParlayEvaluateRequest(BaseModel):
    legs: List[ParlayLegInput]
    num_simulations: int = 10000


class EvaluatedLeg(BaseModel):
    match_id: str
    player_id: Optional[str] = None
    market: str
    selection: str
    line: Optional[float] = None
    individual_probability: float
    fair_odds: float
    market_odds: float
    ev: float
    is_weak_leg: bool
    diagnostic: str
    suggested_alternative: Optional[str] = None


class ParlayEvaluateResponse(BaseModel):
    joint_probability: float
    independent_probability: float
    correlation_penalty: float
    fair_odds: float
    bookmaker_odds: float
    expected_value: float
    edge_percentage: float
    num_simulations: int
    risk_assessment: str
    legs: List[EvaluatedLeg]
    warnings: List[str] = []


class DailyParlayItem(BaseModel):
    tier: RiskTier
    title: str
    joint_probability: float
    fair_odds: float
    bookmaker_odds: float
    expected_value: float
    legs_count: int
    rationale: str
    legs: List[EvaluatedLeg]


class DailyParlayResponse(BaseModel):
    generated_at: str
    conservative: DailyParlayItem
    balanced: DailyParlayItem
    high_yield: DailyParlayItem
