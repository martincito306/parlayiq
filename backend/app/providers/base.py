from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime


class SportsDataProvider(ABC):
    """
    Unified abstract interface for sports data providers in PARLAYIQ.
    All data providers must implement these methods and return standardized payloads
    with metadata (source, updated_at, data_status, confidence_score).
    """

    @abstractmethod
    async def get_competitions(self) -> List[Dict[str, Any]]:
        """List active competitions/leagues."""
        pass

    @abstractmethod
    async def get_today_matches(self) -> List[Dict[str, Any]]:
        """Matches scheduled for today."""
        pass

    @abstractmethod
    async def get_live_matches(self) -> List[Dict[str, Any]]:
        """Matches currently in play."""
        pass

    @abstractmethod
    async def get_fixtures(self, competition_code: str, date_from: Optional[str] = None, date_to: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fixtures for a competition."""
        pass

    @abstractmethod
    async def get_match_details(self, match_id: str) -> Optional[Dict[str, Any]]:
        """Complete match overview, status, score."""
        pass

    @abstractmethod
    async def get_team_statistics(self, team_id: str) -> Dict[str, Any]:
        """Team performance metrics (goals, shots, corners, cards)."""
        pass

    @abstractmethod
    async def get_player_statistics(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Player performance metrics (shots, sot, fouls, rating)."""
        pass

    @abstractmethod
    async def get_player_season_statistics(self, player_id: str) -> Dict[str, Any]:
        """Player season aggregates per 90."""
        pass

    @abstractmethod
    async def get_player_match_history(self, player_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recent matches of player (for L5/L10 hit rate calculation)."""
        pass

    @abstractmethod
    async def get_lineups(self, match_id: str) -> Dict[str, Any]:
        """Starting XI, substitutes, formations."""
        pass

    @abstractmethod
    async def get_match_events(self, match_id: str) -> List[Dict[str, Any]]:
        """Timeline of goals, cards, substitutions, penalties."""
        pass

    @abstractmethod
    async def get_live_statistics(self, match_id: str) -> Dict[str, Any]:
        """In-play stats (possession, shots, attacks, momentum)."""
        pass

    @abstractmethod
    async def get_odds(self, match_id: str) -> List[Dict[str, Any]]:
        """Current bookmaker odds across markets."""
        pass

    @abstractmethod
    async def get_odds_history(self, match_id: str) -> List[Dict[str, Any]]:
        """Historical odds tracking for Closing Line Value (CLV)."""
        pass

    @abstractmethod
    async def get_injuries(self, team_id: str) -> List[Dict[str, Any]]:
        """List of injured players."""
        pass

    @abstractmethod
    async def get_suspensions(self, team_id: str) -> List[Dict[str, Any]]:
        """List of suspended players."""
        pass
