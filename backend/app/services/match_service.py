from typing import List, Dict, Any, Optional
from app.providers.factory import data_provider
from app.engine.poisson_model import DixonColesGoalModel
from app.engine.corners_model import CornersEngine
from app.engine.cards_model import CardsEngine
from app.engine.confidence_model import ConfidenceEngine
from app.models.base import DataStatus


class MatchService:
    def __init__(self):
        self.goal_model = DixonColesGoalModel(rho=-0.11, max_goals=7)

    async def get_today_matches(self) -> List[Dict[str, Any]]:
        matches = await data_provider.get_today_matches()
        return matches

    async def get_live_matches(self) -> List[Dict[str, Any]]:
        return await data_provider.get_live_matches()

    async def get_match_analysis(self, match_id: str) -> Optional[Dict[str, Any]]:
        match = await data_provider.get_match_details(match_id)
        if not match:
            return None

        home = match["home_team"]
        away = match["away_team"]

        # Calculate lambda (home expected goals) and mu (away expected goals)
        # lambda = home_attack * away_defense * home_advantage (1.18)
        # mu = away_attack * home_defense
        lambda_home = home.get("attack_rating", 1.2) * away.get("defense_rating", 0.9) * 1.18
        mu_away = away.get("attack_rating", 1.1) * home.get("defense_rating", 0.8)

        # 1. Goal markets
        goal_markets = self.goal_model.calculate_match_markets(lambda_home, mu_away)

        # 2. Corners markets
        corner_markets = CornersEngine.calculate_corner_markets(
            home_corners_for=home.get("avg_corners", 6.5),
            home_corners_against=4.5,
            away_corners_for=away.get("avg_corners", 5.5),
            away_corners_against=5.0
        )

        # 3. Cards markets
        card_markets = CardsEngine.calculate_card_markets(
            home_cards_avg=home.get("avg_cards", 1.9),
            away_cards_avg=away.get("avg_cards", 2.2),
            referee_cards_avg=4.3,
            is_derby=("Clásico" in match.get("competition_name", "") or "Derby" in match.get("id", ""))
        )

        # 4. Data Quality & Confidence
        confidence = ConfidenceEngine.evaluate_match_data_quality(
            lineup_confirmed=True,
            matches_sample_size=28,
            data_status=DataStatus(match.get("data_status", "PROVISIONAL_SYNTHETIC")),
            has_odds=len(match.get("odds", [])) > 0
        )

        # 5. Extract market opportunities with Positive EV
        opportunities = []
        odds_list = match.get("odds", [])
        
        # Check Over 2.5 Goals
        over_2_5_prob = goal_markets["over_2_5"]
        for o in odds_list:
            if o.get("market") == "TOTAL_GOALS" and o.get("selection") == "OVER_2.5":
                ev = (over_2_5_prob * o["odd_value"]) - 1.0
                fair_odd = round(1.0 / over_2_5_prob, 2)
                opportunities.append({
                    "market": "Total Goles",
                    "selection": "Más de 2.5",
                    "calculated_probability": over_2_5_prob,
                    "fair_odds": fair_odd,
                    "market_odds": o["odd_value"],
                    "ev": round(ev, 4),
                    "is_value": ev > 0,
                    "edge_pct": round(((over_2_5_prob - (1.0 / o["odd_value"])) * o["odd_value"]) * 100, 2)
                })

        # Check Home Win
        home_win_prob = goal_markets["home_win"]
        for o in odds_list:
            if o.get("market") == "1X2" and o.get("selection") == "HOME":
                ev = (home_win_prob * o["odd_value"]) - 1.0
                fair_odd = round(1.0 / home_win_prob, 2)
                opportunities.append({
                    "market": "Resultado Final (1X2)",
                    "selection": f"Victoria {home['name']}",
                    "calculated_probability": home_win_prob,
                    "fair_odds": fair_odd,
                    "market_odds": o["odd_value"],
                    "ev": round(ev, 4),
                    "is_value": ev > 0,
                    "edge_pct": round(((home_win_prob - (1.0 / o["odd_value"])) * o["odd_value"]) * 100, 2)
                })

        return {
            "match": match,
            "lambda_home": round(lambda_home, 2),
            "mu_away": round(mu_away, 2),
            "goal_markets": goal_markets,
            "corner_markets": corner_markets,
            "card_markets": card_markets,
            "confidence": confidence,
            "opportunities": opportunities,
            "odds": odds_list
        }


match_service = MatchService()
