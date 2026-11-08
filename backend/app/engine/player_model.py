import numpy as np
from typing import Dict, Any, Optional
from app.engine.negative_binomial import OverdispersedCountModel


class PlayerPropsEngine:
    """
    Quantitative evaluation of individual player markets:
    - Shots total & Shots on Target (SOT)
    - Fouls committed & Cards
    - Anytime goalscorer
    Accounts for expected minutes, opponent defensive allowance, and home/away factor.
    """
    
    @staticmethod
    def evaluate_player(
        player_name: str,
        position: str,
        shots_per_90: float,
        sot_per_90: float,
        goals_per_90: float,
        fouls_per_90: float,
        expected_minutes: float = 80.0,
        is_home: bool = True,
        opponent_conceded_shots_ratio: float = 1.0,  # 1.15 = weak defense, 0.85 = elite defense
        l5_shots_hit_rate: float = 0.80,
        l10_shots_hit_rate: float = 0.70,
    ) -> Dict[str, Any]:
        """
        Calculates true probability of exceeding lines considering context.
        """
        # 1. Expected minutes ratio
        minutes_factor = min(1.0, max(0.2, expected_minutes / 90.0))
        
        # 2. Home advantage boost for shooting (typically ~6-10% more shots at home)
        venue_factor = 1.06 if is_home else 0.94
        
        # 3. Adjusted lambda parameters
        effective_shots_mean = shots_per_90 * minutes_factor * venue_factor * opponent_conceded_shots_ratio
        effective_sot_mean = sot_per_90 * minutes_factor * venue_factor * opponent_conceded_shots_ratio
        effective_goals_mean = goals_per_90 * minutes_factor * venue_factor * opponent_conceded_shots_ratio
        effective_fouls_mean = fouls_per_90 * minutes_factor * (0.95 if is_home else 1.05)
        
        # 4. Football shooting variance is ~1.3 - 1.5x the mean (overdispersed)
        shots_var = effective_shots_mean * 1.42
        sot_var = effective_sot_mean * 1.35
        fouls_var = effective_fouls_mean * 1.25
        
        shots_eval = OverdispersedCountModel.calculate_exceedance_probabilities(
            effective_shots_mean, shots_var, lines=[0.5, 1.5, 2.5, 3.5]
        )
        sot_eval = OverdispersedCountModel.calculate_exceedance_probabilities(
            effective_sot_mean, sot_var, lines=[0.5, 1.5, 2.5]
        )
        fouls_eval = OverdispersedCountModel.calculate_exceedance_probabilities(
            effective_fouls_mean, fouls_var, lines=[0.5, 1.5, 2.5]
        )
        
        # 5. Anytime Goalscorer probability: 1 - exp(-effective_goals_mean)
        goal_prob = float(1.0 - np.exp(-effective_goals_mean))
        goal_fair_odds = round(1.0 / max(0.001, goal_prob), 2)
        
        return {
            "player_name": player_name,
            "position": position,
            "expected_minutes": expected_minutes,
            "effective_shots_per_game": round(effective_shots_mean, 2),
            "effective_sot_per_game": round(effective_sot_mean, 2),
            "shots_markets": shots_eval["lines"],
            "sot_markets": sot_eval["lines"],
            "fouls_markets": fouls_eval["lines"],
            "anytime_goal": {
                "probability": round(goal_prob, 4),
                "fair_odds": goal_fair_odds
            },
            "historical_form": {
                "l5_shots_over_1_5": l5_shots_hit_rate,
                "l10_shots_over_1_5": l10_shots_hit_rate
            }
        }
