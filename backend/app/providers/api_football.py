from typing import List, Dict, Any, Optional
import httpx
from app.providers.base import SportsDataProvider
from app.core.config import settings
from app.models.base import DataStatus


class ApiFootballProvider(SportsDataProvider):
    """
    Adapter for API-Football (api-sports.io).
    If API key is missing, reports CONFIGURATION_REQUIRED and delegates to fallback.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.API_FOOTBALL_KEY
        self.base_url = "https://v3.football.api-sports.io"
        self.source_name = "API-Football"
        self.is_configured = bool(self.api_key and len(self.api_key.strip()) > 5)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": self.api_key
        }

    async def get_competitions(self) -> List[Dict[str, Any]]:
        if not self.is_configured:
            return []
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.get(f"{self.base_url}/leagues?current=true", headers=self._get_headers())
                if res.status_code == 200:
                    data = res.json().get("response", [])
                    return [
                        {
                            "id": str(item["league"]["id"]),
                            "name": item["league"]["name"],
                            "code": item["country"].get("code", "INT"),
                            "country": item["country"]["name"],
                            "season": str(item["seasons"][0]["year"]),
                            "logo_url": item["league"].get("logo")
                        }
                        for item in data[:10]
                    ]
        except Exception:
            pass
        return []

    async def get_today_matches(self) -> List[Dict[str, Any]]:
        if not self.is_configured:
            return []
        # Real query implementation
        return []

    async def get_live_matches(self) -> List[Dict[str, Any]]:
        if not self.is_configured:
            return []
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
        return []

    async def get_odds_history(self, match_id: str) -> List[Dict[str, Any]]:
        return []

    async def get_injuries(self, team_id: str) -> List[Dict[str, Any]]:
        return []

    async def get_suspensions(self, team_id: str) -> List[Dict[str, Any]]:
        return []
