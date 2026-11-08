from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class AIChatRequest(BaseModel):
    message: str
    match_id: Optional[str] = None
    player_id: Optional[str] = None
    include_simulation: bool = True


class AIChatResponse(BaseModel):
    reply: str
    match_analysis: Optional[Dict[str, Any]] = None
    recommended_markets: List[Dict[str, Any]] = []
    risks_identified: List[str] = []
    data_source: str = "football-data.co.uk / Opta-Equivalent Model"
    confidence_level: str = "HIGH"
