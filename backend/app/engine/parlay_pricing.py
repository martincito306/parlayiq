from typing import Dict, Any, List
from app.models.predictions import RiskTier


class ParlayPricingEngine:
    """
    Pricing, Overround, and Expected Value (EV) evaluation for sports bets and parlays.
    Formula: EV = (Probability * Odds) - 1.0
    """
    @staticmethod
    def calculate_ev(probability: float, bookmaker_odds: float) -> float:
        """Calculates expected return per 1 unit wagered."""
        return (probability * bookmaker_odds) - 1.0

    @staticmethod
    def calculate_fair_odds(probability: float) -> float:
        """Returns fair decimal odds without house margin."""
        if probability <= 0:
            return 999.0
        return round(1.0 / probability, 2)

    @staticmethod
    def calculate_kelly_fraction(probability: float, decimal_odds: float, bankroll_fraction: float = 0.25) -> float:
        """
        Calculates Fractional Kelly Criterion for risk management.
        b = decimal_odds - 1
        f* = (p * b - (1 - p)) / b
        """
        b = decimal_odds - 1.0
        if b <= 0 or probability <= 0:
            return 0.0
        q = 1.0 - probability
        kelly = (probability * b - q) / b
        if kelly <= 0:
            return 0.0
        return round(kelly * bankroll_fraction, 4)

    @staticmethod
    def evaluate_pricing(joint_probability: float, bookmaker_odds: float) -> Dict[str, Any]:
        """
        Complete pricing evaluation of a ticket or individual selection.
        """
        fair_odds = ParlayPricingEngine.calculate_fair_odds(joint_probability)
        ev = ParlayPricingEngine.calculate_ev(joint_probability, bookmaker_odds)
        implied_prob = round(1.0 / max(1.01, bookmaker_odds), 4)
        edge_pct = round(((joint_probability - implied_prob) / implied_prob) * 100.0, 2)
        kelly_rec = ParlayPricingEngine.calculate_kelly_fraction(joint_probability, bookmaker_odds)

        if joint_probability >= 0.55:
            risk_tier = RiskTier.CONSERVATIVE
        elif joint_probability >= 0.30:
            risk_tier = RiskTier.BALANCED
        else:
            risk_tier = RiskTier.HIGH_YIELD

        is_positive_value = ev > 0.0

        return {
            "joint_probability": round(joint_probability, 4),
            "implied_probability": implied_prob,
            "fair_odds": fair_odds,
            "bookmaker_odds": round(bookmaker_odds, 2),
            "expected_value": round(ev, 4),
            "edge_percentage": edge_pct,
            "is_positive_value": is_positive_value,
            "recommended_kelly_stake_pct": round(kelly_rec * 100.0, 2),
            "risk_tier": risk_tier.value
        }
