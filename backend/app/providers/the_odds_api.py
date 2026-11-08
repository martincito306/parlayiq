from typing import List, Dict, Any, Optional
import httpx
from app.providers.base import SportsDataProvider
from app.core.config import settings
from app.models.base import DataStatus


class TheOddsApiProvider(SportsDataProvider):
    """
    Adapter for The Odds API (real bookmaker odds from Pinnacle, Bet365, DraftKings).
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.THE_ODDS_API_KEY
        self.base_url = "https://api.the-odds-api.com/v4"
        self.source_name = "The Odds API"
        self.is_configured = bool(self.api_key and len(self.api_key.strip()) > 5)

    async def get_competitions(self) -> List[Dict[str, Any]]:
        return []

    async def get_today_matches(self) -> List[Dict[str, Any]]:
        return []

    async def get_live_matches(self) -> List[Dict[str, Any]]:
        return []

    async def get_fixtures(self, competition_code: str, date_from: Optional[str] = None, date_to: Optional[str] = None) -> List[Dict[str, Any]]:
        return []

    async def get_match_details(self, match_id: str) -> Optional[Dict[str, Any]]:
        return None

    async def get_team_statistics(self, team_id: str) -> Dict[str, Any]:
        return {}

    async def get_player_statistics(self, player_id: str) -> Optional[Dict[str, Any]]:
        return None

    async def get_player_season_statistics(self, player_id: str) -> Dict[str, Any]:
        return {}

    async def get_player_match_history(self, player_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        return []

    async def get_lineups(self, match_id: str) -> Dict[str, Any]:
        return {}

    async def get_match_events(self, match_id: str) -> List[Dict[str, Any]]:
        return []

    async def get_live_statistics(self, match_id: str) -> Dict[str, Any]:
        return {}

    async def get_odds(self, match_id: str) -> List[Dict[str, Any]]:
        if not self.is_configured:
            return []
        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                res = await client.get(
                    f"{self.base_url}/sports/soccer/odds",
                    params={"apiKey": self.api_key, "regions": "eu,uk", "markets": "h2h,totals"}
                )
                if res.status_code == 200:
                    return res.json()
        except Exception:
            pass
        return []

    async def get_odds_history(self, match_id: str) -> List[Dict[str, Any]]:
        return []

    async def get_injuries(self, team_id: str) -> List[Dict[str, Any]]:
        return []

    async def get_suspensions(self, team_id: str) -> List[Dict[str, Any]]:
        return []
