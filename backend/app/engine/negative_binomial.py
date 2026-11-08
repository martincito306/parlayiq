import numpy as np
from scipy.stats import nbinom, poisson
from typing import Dict, Any


class OverdispersedCountModel:
    """
    Negative Binomial model for overdispersed football counts:
    - Player shots and shots on target
    - Team and match corners
    - Fouls and yellow/red cards
    """
    @staticmethod
    def fit_parameters(mean: float, variance: float) -> tuple[float, float, bool]:
        """
        Derives Negative Binomial (n, p) from empirical mean and variance.
        If variance <= mean, returns Poisson fallback.
        """
        mean = max(0.01, mean)
        if variance > mean * 1.05:
            # Overdispersed -> Negative Binomial
            n = (mean ** 2) / (variance - mean)
            p = n / (n + mean)
            return float(n), float(p), True
        else:
            # Low dispersion -> Poisson equivalent
            return mean, 1.0, False

    @staticmethod
    def calculate_exceedance_probabilities(
        mean: float,
        variance: float,
        lines: list[float] = [0.5, 1.5, 2.5, 3.5, 4.5]
    ) -> Dict[str, Any]:
        """
        Calculates P(X > line) for specified thresholds.
        """
        n, p, is_nbinom = OverdispersedCountModel.fit_parameters(mean, variance)
        
        results = {}
        for line in lines:
            k = int(np.floor(line))
            if is_nbinom:
                # P(X <= k) = nbinom.cdf(k, n, p)
                prob_under = float(nbinom.cdf(k, n, p))
            else:
                prob_under = float(poisson.cdf(k, mean))
            
            prob_over = max(0.0001, min(0.9999, 1.0 - prob_under))
            fair_odds = round(1.0 / prob_over, 2)
            results[f"over_{line}"] = {
                "probability": round(prob_over, 4),
                "fair_odds": fair_odds,
                "under_probability": round(prob_under, 4),
                "under_fair_odds": round(1.0 / max(0.0001, prob_under), 2)
            }
            
        return {
            "mean": round(mean, 2),
            "variance": round(variance, 2),
            "is_overdispersed": is_nbinom,
            "lines": results
        }
