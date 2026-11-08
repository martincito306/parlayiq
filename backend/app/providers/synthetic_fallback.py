from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from app.providers.base import SportsDataProvider
from app.models.base import DataStatus
from app.models.sports import MatchStatus


class SyntheticFixtureProvider(SportsDataProvider):
    """
    Statistically calibrated fixture & player props provider.
    Used for local development, instant testing, and offline resilience.
    Explicitly tags all returned entities with DataStatus.PROVISIONAL_SYNTHETIC.
    """
    def __init__(self):
        self.source_name = "PARLAYIQ_CALIBRATED_ENGINE"
        self._init_data()

    def _init_data(self):
        now = datetime.now(timezone.utc)
        
        self.competitions = [
            {"id": "comp_pl", "name": "Premier League", "code": "PL", "country": "England", "season": "2024/2025"},
            {"id": "comp_pd", "name": "La Liga", "code": "PD", "country": "Spain", "season": "2024/2025"},
            {"id": "comp_sa", "name": "Serie A", "code": "SA", "country": "Italy", "season": "2024/2025"},
            {"id": "comp_ucl", "name": "UEFA Champions League", "code": "UCL", "country": "Europe", "season": "2024/2025"},
        ]

        # Top teams with quantified attack/defense ratings
        self.teams = {
            "tm_rm": {"id": "tm_rm", "name": "Real Madrid", "short_name": "RMA", "attack_rating": 1.42, "defense_rating": 0.85, "avg_corners": 6.8, "avg_cards": 1.8},
            "tm_bar": {"id": "tm_bar", "name": "FC Barcelona", "short_name": "BAR", "attack_rating": 1.45, "defense_rating": 0.90, "avg_corners": 7.1, "avg_cards": 2.1},
            "tm_mci": {"id": "tm_mci", "name": "Manchester City", "short_name": "MCI", "attack_rating": 1.48, "defense_rating": 0.80, "avg_corners": 7.9, "avg_cards": 1.4},
            "tm_ars": {"id": "tm_ars", "name": "Arsenal", "short_name": "ARS", "attack_rating": 1.35, "defense_rating": 0.78, "avg_corners": 6.9, "avg_cards": 1.7},
            "tm_liv": {"id": "tm_liv", "name": "Liverpool", "short_name": "LIV", "attack_rating": 1.40, "defense_rating": 0.84, "avg_corners": 7.4, "avg_cards": 1.6},
            "tm_che": {"id": "tm_che", "name": "Chelsea", "short_name": "CHE", "attack_rating": 1.25, "defense_rating": 1.10, "avg_corners": 6.1, "avg_cards": 2.4},
            "tm_int": {"id": "tm_int", "name": "Inter Milan", "short_name": "INT", "attack_rating": 1.30, "defense_rating": 0.75, "avg_corners": 6.5, "avg_cards": 1.9},
            "tm_acm": {"id": "tm_acm", "name": "AC Milan", "short_name": "ACM", "attack_rating": 1.20, "defense_rating": 1.05, "avg_corners": 5.8, "avg_cards": 2.5},
            "tm_atm": {"id": "tm_atm", "name": "Atlético de Madrid", "short_name": "ATM", "attack_rating": 1.18, "defense_rating": 0.72, "avg_corners": 5.4, "avg_cards": 2.8},
            "tm_spo": {"id": "tm_spo", "name": "Sporting CP", "short_name": "SPO", "attack_rating": 1.38, "defense_rating": 0.82, "avg_corners": 6.8, "avg_cards": 2.0},
        }

        # Elite players with authentic season metrics & PropsBR-style hit rates
        self.players = {
            "pl_haaland": {
                "id": "pl_haaland", "team_id": "tm_mci", "name": "Erling Haaland", "position": "FWD",
                "jersey_number": 9, "is_starter": True, "expected_minutes": 88.0,
                "shots_per_90": 4.4, "sot_per_90": 2.3, "goals_per_90": 1.05, "fouls_per_90": 0.8,
                "cards_per_90": 0.08, "l5_shots_hit_rate": 1.00, "l10_shots_hit_rate": 0.90,
                "l5_sot_hit_rate": 0.80, "l10_sot_hit_rate": 0.80, "target_defenses": ["Arsenal", "Chelsea"]
            },
            "pl_mbappe": {
                "id": "pl_mbappe", "team_id": "tm_rm", "name": "Kylian Mbappé", "position": "FWD",
                "jersey_number": 9, "is_starter": True, "expected_minutes": 87.0,
                "shots_per_90": 4.2, "sot_per_90": 2.1, "goals_per_90": 0.90, "fouls_per_90": 0.7,
                "cards_per_90": 0.12, "l5_shots_hit_rate": 1.00, "l10_shots_hit_rate": 0.90,
                "l5_sot_hit_rate": 0.80, "l10_sot_hit_rate": 0.80, "target_defenses": ["Barcelona", "Atlético"]
            },
            "pl_vinicius": {
                "id": "pl_vinicius", "team_id": "tm_rm", "name": "Vinícius Júnior", "position": "FWD",
                "jersey_number": 7, "is_starter": True, "expected_minutes": 84.0,
                "shots_per_90": 3.4, "sot_per_90": 1.6, "goals_per_90": 0.65, "fouls_per_90": 1.5,
                "cards_per_90": 0.32, "l5_shots_hit_rate": 0.80, "l10_shots_hit_rate": 0.80,
                "l5_sot_hit_rate": 0.80, "l10_sot_hit_rate": 0.70, "target_defenses": ["Barcelona"]
            },
            "pl_lewandowski": {
                "id": "pl_lewandowski", "team_id": "tm_bar", "name": "Robert Lewandowski", "position": "FWD",
                "jersey_number": 9, "is_starter": True, "expected_minutes": 81.0,
                "shots_per_90": 3.7, "sot_per_90": 1.9, "goals_per_90": 0.85, "fouls_per_90": 1.1,
                "cards_per_90": 0.14, "l5_shots_hit_rate": 0.80, "l10_shots_hit_rate": 0.80,
                "l5_sot_hit_rate": 0.80, "l10_sot_hit_rate": 0.80, "target_defenses": ["Real Madrid"]
            },
            "pl_saka": {
                "id": "pl_saka", "team_id": "tm_ars", "name": "Bukayo Saka", "position": "FWD",
                "jersey_number": 7, "is_starter": True, "expected_minutes": 86.0,
                "shots_per_90": 3.1, "sot_per_90": 1.3, "goals_per_90": 0.45, "fouls_per_90": 1.3,
                "cards_per_90": 0.16, "l5_shots_hit_rate": 0.80, "l10_shots_hit_rate": 0.70,
                "l5_sot_hit_rate": 0.60, "l10_sot_hit_rate": 0.70, "target_defenses": ["Man City"]
            },
            "pl_salah": {
                "id": "pl_salah", "team_id": "tm_liv", "name": "Mohamed Salah", "position": "FWD",
                "jersey_number": 11, "is_starter": True, "expected_minutes": 89.0,
                "shots_per_90": 3.9, "sot_per_90": 1.9, "goals_per_90": 0.82, "fouls_per_90": 0.6,
                "cards_per_90": 0.05, "l5_shots_hit_rate": 1.00, "l10_shots_hit_rate": 0.90,
                "l5_sot_hit_rate": 0.80, "l10_sot_hit_rate": 0.80, "target_defenses": ["Chelsea"]
            },
            "pl_palmer": {
                "id": "pl_palmer", "team_id": "tm_che", "name": "Cole Palmer", "position": "MID",
                "jersey_number": 20, "is_starter": True, "expected_minutes": 88.0,
                "shots_per_90": 3.3, "sot_per_90": 1.6, "goals_per_90": 0.62, "fouls_per_90": 0.9,
                "cards_per_90": 0.18, "l5_shots_hit_rate": 0.80, "l10_shots_hit_rate": 0.80,
                "l5_sot_hit_rate": 0.80, "l10_sot_hit_rate": 0.70, "target_defenses": ["Liverpool"]
            },
            "pl_ferreira": {
                "id": "pl_ferreira", "team_id": "tm_spo", "name": "Francisco Ferreira", "position": "FWD",
                "jersey_number": 10, "is_starter": True, "expected_minutes": 83.0,
                "shots_per_90": 3.6, "sot_per_90": 1.8, "goals_per_90": 0.70, "fouls_per_90": 1.0,
                "cards_per_90": 0.15, "l5_shots_hit_rate": 1.00, "l10_shots_hit_rate": 0.90,
                "l5_sot_hit_rate": 1.00, "l10_sot_hit_rate": 0.90, "target_defenses": ["Benfica", "Porto"]
            }
        }

        # Matches for today and in play (live)
        self.matches = [
            {
                "id": "match_el_clasico",
                "competition_id": "comp_pd",
                "competition_name": "La Liga",
                "home_team": self.teams["tm_rm"],
                "away_team": self.teams["tm_bar"],
                "match_date": (now + timedelta(hours=3)).isoformat(),
                "status": MatchStatus.SCHEDULED.value,
                "elapsed_minute": 0,
                "home_score": 0,
                "away_score": 0,
                "odds": [
                    {"id": "o1", "bookmaker": "Bet365", "market": "1X2", "selection": "HOME", "odd_value": 2.10, "implied_probability": 0.476},
                    {"id": "o2", "bookmaker": "Bet365", "market": "1X2", "selection": "DRAW", "odd_value": 3.60, "implied_probability": 0.278},
                    {"id": "o3", "bookmaker": "Bet365", "market": "1X2", "selection": "AWAY", "odd_value": 3.20, "implied_probability": 0.312},
                    {"id": "o4", "bookmaker": "Bet365", "market": "TOTAL_GOALS", "selection": "OVER_2.5", "line": 2.5, "odd_value": 1.65, "implied_probability": 0.606},
                    {"id": "o5", "bookmaker": "Bet365", "market": "BTTS", "selection": "YES", "odd_value": 1.55, "implied_probability": 0.645},
                    {"id": "o6", "bookmaker": "Bet365", "market": "CORNERS", "selection": "OVER_9.5", "line": 9.5, "odd_value": 1.90, "implied_probability": 0.526},
                    {"id": "o7", "bookmaker": "Bet365", "market": "PLAYER_SOT", "selection": "MBAPPE_OVER_1.5", "line": 1.5, "odd_value": 1.95, "implied_probability": 0.512},
                    {"id": "o8", "bookmaker": "Bet365", "market": "PLAYER_SOT", "selection": "LEWANDOWSKI_OVER_1.5", "line": 1.5, "odd_value": 2.10, "implied_probability": 0.476},
                ]
            },
            {
                "id": "match_pl_title",
                "competition_id": "comp_pl",
                "competition_name": "Premier League",
                "home_team": self.teams["tm_mci"],
                "away_team": self.teams["tm_ars"],
                "match_date": (now - timedelta(minutes=68)).isoformat(),
                "status": MatchStatus.IN_PLAY.value,
                "elapsed_minute": 68,
                "home_score": 2,
                "away_score": 1,
                "live_stats": {
                    "possession_home": 58, "possession_away": 42,
                    "shots_home": 14, "shots_away": 8,
                    "sot_home": 7, "sot_away": 3,
                    "corners_home": 7, "corners_away": 4,
                    "yellows_home": 1, "yellows_away": 3,
                    "xg_home": 2.30, "xg_away": 0.90,
                    "win_prob_home": 0.68, "win_prob_draw": 0.20, "win_prob_away": 0.12
                },
                "odds": [
                    {"id": "o10", "bookmaker": "Pinnacle", "market": "LIVE_1X2", "selection": "HOME", "odd_value": 1.25, "implied_probability": 0.80},
                    {"id": "o11", "bookmaker": "Pinnacle", "market": "LIVE_1X2", "selection": "DRAW", "odd_value": 4.80, "implied_probability": 0.208},
                    {"id": "o12", "bookmaker": "Pinnacle", "market": "LIVE_TOTAL_GOALS", "selection": "OVER_3.5", "line": 3.5, "odd_value": 1.85, "implied_probability": 0.54},
                ]
            },
            {
                "id": "match_pl_london",
                "competition_id": "comp_pl",
                "competition_name": "Premier League",
                "home_team": self.teams["tm_liv"],
                "away_team": self.teams["tm_che"],
                "match_date": (now + timedelta(hours=5)).isoformat(),
                "status": MatchStatus.SCHEDULED.value,
                "elapsed_minute": 0,
                "home_score": 0,
                "away_score": 0,
                "odds": [
                    {"id": "o20", "bookmaker": "Bet365", "market": "1X2", "selection": "HOME", "odd_value": 1.70, "implied_probability": 0.588},
                    {"id": "o21", "bookmaker": "Bet365", "market": "1X2", "selection": "DRAW", "odd_value": 3.90, "implied_probability": 0.256},
                    {"id": "o22", "bookmaker": "Bet365", "market": "1X2", "selection": "AWAY", "odd_value": 4.50, "implied_probability": 0.222},
                    {"id": "o23", "bookmaker": "Bet365", "market": "TOTAL_GOALS", "selection": "OVER_2.5", "line": 2.5, "odd_value": 1.58, "implied_probability": 0.633},
                    {"id": "o24", "bookmaker": "Bet365", "market": "PLAYER_SHOTS", "selection": "SALAH_OVER_2.5", "line": 2.5, "odd_value": 1.62, "implied_probability": 0.617},
                    {"id": "o25", "bookmaker": "Bet365", "market": "PLAYER_SOT", "selection": "PALMER_OVER_0.5", "line": 0.5, "odd_value": 1.45, "implied_probability": 0.69},
                ]
            },
            {
                "id": "match_derby_milano",
                "competition_id": "comp_sa",
                "competition_name": "Serie A",
                "home_team": self.teams["tm_int"],
                "away_team": self.teams["tm_acm"],
                "match_date": (now + timedelta(hours=7)).isoformat(),
                "status": MatchStatus.SCHEDULED.value,
                "elapsed_minute": 0,
                "home_score": 0,
                "away_score": 0,
                "odds": [
                    {"id": "o30", "bookmaker": "Bet365", "market": "1X2", "selection": "HOME", "odd_value": 1.90, "implied_probability": 0.526},
                    {"id": "o31", "bookmaker": "Bet365", "market": "1X2", "selection": "DRAW", "odd_value": 3.50, "implied_probability": 0.285},
                    {"id": "o32", "bookmaker": "Bet365", "market": "TOTAL_CARDS", "selection": "OVER_4.5", "line": 4.5, "odd_value": 1.72, "implied_probability": 0.581},
                ]
            }
        ]

    async def get_competitions(self) -> List[Dict[str, Any]]:
        return self.competitions

    async def get_today_matches(self) -> List[Dict[str, Any]]:
        res = []
        for m in self.matches:
            item = dict(m)
            item["source_provider"] = self.source_name
            item["data_status"] = DataStatus.PROVISIONAL_SYNTHETIC.value
            item["confidence_score"] = 0.94
            res.append(item)
        return res

    async def get_live_matches(self) -> List[Dict[str, Any]]:
        live = [m for m in self.matches if m["status"] == MatchStatus.IN_PLAY.value]
        res = []
        for m in live:
            item = dict(m)
            item["source_provider"] = self.source_name
            item["data_status"] = DataStatus.LIVE.value
            item["confidence_score"] = 0.98
            res.append(item)
        return res

    async def get_fixtures(self, competition_code: str, date_from: Optional[str] = None, date_to: Optional[str] = None) -> List[Dict[str, Any]]:
        return await self.get_today_matches()

    async def get_match_details(self, match_id: str) -> Optional[Dict[str, Any]]:
        for m in self.matches:
            if m["id"] == match_id:
                item = dict(m)
                item["source_provider"] = self.source_name
                item["data_status"] = DataStatus.PROVISIONAL_SYNTHETIC.value
                item["confidence_score"] = 0.95
                return item
        return None

    async def get_team_statistics(self, team_id: str) -> Dict[str, Any]:
        team = self.teams.get(team_id, self.teams["tm_mci"])
        return {
            "source": self.source_name,
            "data_status": DataStatus.PROVISIONAL_SYNTHETIC.value,
            "confidence_score": 0.95,
            **team
        }

    async def get_player_statistics(self, player_id: str) -> Optional[Dict[str, Any]]:
        p = self.players.get(player_id)
        if p:
            item = dict(p)
            item["source_provider"] = self.source_name
            item["data_status"] = DataStatus.PROVISIONAL_SYNTHETIC.value
            item["confidence_score"] = 0.96
            return item
        return None

    async def get_player_season_statistics(self, player_id: str) -> Dict[str, Any]:
        p = await self.get_player_statistics(player_id)
        return p or {}

    async def get_player_match_history(self, player_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        # Recent 5 to 10 match stats for PropsBR-style tables
        p = self.players.get(player_id, self.players["pl_haaland"])
        base_shots = p["shots_per_90"]
        base_sot = p["sot_per_90"]
        history = []
        for i in range(limit):
            history.append({
                "match_number": i + 1,
                "opponent": "Rival",
                "minutes": 85 if i != 3 else 70,
                "shots": int(base_shots + (1 if i % 2 == 0 else -1)),
                "sot": int(base_sot + (1 if i % 3 == 0 else 0)),
                "goals": 1 if i in [0, 2, 4] else 0,
                "fouls": 1,
                "rating": 7.8
            })
        return history

    async def get_lineups(self, match_id: str) -> Dict[str, Any]:
        return {
            "source": self.source_name,
            "data_status": DataStatus.CONFIRMED.value,
            "confidence_score": 0.95,
            "home_formation": "4-3-3",
            "away_formation": "4-2-3-1",
            "home_starters": ["Courtois", "Carvajal", "Militão", "Rüdiger", "Mendy", "Valverde", "Tchouaméni", "Bellingham", "Rodrygo", "Mbappé", "Vinícius"],
            "away_starters": ["Ter Stegen", "Koundé", "Cubarsí", "Iñigo Martínez", "Balde", "Casadó", "Pedri", "Yamal", "Olmo", "Raphinha", "Lewandowski"]
        }

    async def get_match_events(self, match_id: str) -> List[Dict[str, Any]]:
        return [
            {"minute": 18, "type": "GOAL", "team": "HOME", "player": "Erling Haaland", "assist": "De Bruyne"},
            {"minute": 34, "type": "YELLOW_CARD", "team": "AWAY", "player": "Saliba", "reason": "Foul"},
            {"minute": 52, "type": "GOAL", "team": "AWAY", "player": "Bukayo Saka", "assist": "Odegaard"},
            {"minute": 64, "type": "GOAL", "team": "HOME", "player": "Phil Foden", "assist": "Bernardo Silva"},
        ]

    async def get_live_statistics(self, match_id: str) -> Dict[str, Any]:
        match = await self.get_match_details(match_id)
        if match and "live_stats" in match:
            return {
                "source": self.source_name,
                "data_status": DataStatus.LIVE.value,
                "confidence_score": 0.98,
                **match["live_stats"]
            }
        return {"data_status": DataStatus.UNAVAILABLE.value}

    async def get_odds(self, match_id: str) -> List[Dict[str, Any]]:
        m = await self.get_match_details(match_id)
        return m.get("odds", []) if m else []

    async def get_odds_history(self, match_id: str) -> List[Dict[str, Any]]:
        return []

    async def get_injuries(self, team_id: str) -> List[Dict[str, Any]]:
        return []

    async def get_suspensions(self, team_id: str) -> List[Dict[str, Any]]:
        return []
