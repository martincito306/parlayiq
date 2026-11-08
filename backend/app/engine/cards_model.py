from typing import Dict, Any
from app.engine.negative_binomial import OverdispersedCountModel


class CardsEngine:
    """
    Evaluates bookings and yellow/red cards probabilities.
    Accounts for referee strictness, derby rivalry factor, and team foul averages.
    """
    @staticmethod
    def calculate_card_markets(
        home_cards_avg: float,
        away_cards_avg: float,
        referee_cards_avg: float = 4.2,
        is_derby: bool = False,
        league_avg_cards: float = 4.1,
    ) -> Dict[str, Any]:
        # Baseline cards
        base = (home_cards_avg + away_cards_avg) / 2.0 * 2.0
        # Referee factor
        ref_factor = referee_cards_avg / max(2.0, league_avg_cards)
        # Derby intensity factor
        derby_factor = 1.22 if is_derby else 1.0
        
        expected_cards = base * ref_factor * derby_factor
        # Card variance is approx 1.35x
        cards_var = expected_cards * 1.35
        
        eval_result = OverdispersedCountModel.calculate_exceedance_probabilities(
            expected_cards, cards_var, lines=[2.5, 3.5, 4.5, 5.5, 6.5]
        )
        
        return {
            "expected_total_cards": round(expected_cards, 2),
            "referee_factor": round(ref_factor, 2),
            "is_derby": is_derby,
            "markets": eval_result["lines"]
        }
