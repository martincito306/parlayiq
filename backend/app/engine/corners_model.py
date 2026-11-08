from typing import Dict, Any
from app.engine.negative_binomial import OverdispersedCountModel


class CornersEngine:
    """
    Evaluates corner kick probabilities for match total and individual teams.
    Corners in top European leagues average ~9.8 - 10.4 per match with high variance (~14.5).
    """
    @staticmethod
    def calculate_corner_markets(
        home_corners_for: float,
        home_corners_against: float,
        away_corners_for: float,
        away_corners_against: float,
        league_avg_corners: float = 10.1,
    ) -> Dict[str, Any]:
        # Synthetic expected corner formula based on attack/defense rates
        home_exp = (home_corners_for + away_corners_against) / 2.0
        away_exp = (away_corners_for + home_corners_against) / 2.0
        total_exp = home_exp + away_exp
        
        # Empirical variance ratio for corner kicks is approx 1.45x
        corners_var = total_exp * 1.45
        
        eval_result = OverdispersedCountModel.calculate_exceedance_probabilities(
            total_exp, corners_var, lines=[7.5, 8.5, 9.5, 10.5, 11.5]
        )
        
        return {
            "expected_corners_home": round(home_exp, 2),
            "expected_corners_away": round(away_exp, 2),
            "expected_total_corners": round(total_exp, 2),
            "markets": eval_result["lines"]
        }
