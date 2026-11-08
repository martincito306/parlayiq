import numpy as np
from scipy.stats import norm
from typing import List, Dict, Tuple


# Empirical baseline correlation lookup between major football markets
# Derived from historical Premier League / La Liga match datasets
MARKET_CORRELATIONS: Dict[Tuple[str, str], float] = {
    ("OVER_GOALS", "BTTS_YES"): 0.62,
    ("OVER_GOALS", "PLAYER_SOT"): 0.45,
    ("OVER_GOALS", "PLAYER_SHOTS"): 0.38,
    ("OVER_GOALS", "OVER_CORNERS"): 0.28,
    ("OVER_GOALS", "UNDER_CORNERS"): -0.25,
    ("OVER_GOALS", "UNDER_GOALS"): -0.95,
    
    ("HOME_WIN", "HOME_OVER_GOALS"): 0.70,
    ("HOME_WIN", "HOME_PLAYER_SOT"): 0.52,
    ("HOME_WIN", "HOME_OVER_CORNERS"): 0.40,
    ("HOME_WIN", "AWAY_WIN"): -0.55,
    
    ("BTTS_YES", "OVER_CORNERS"): 0.22,
    ("BTTS_YES", "BTTS_NO"): -0.99,
    
    ("OVER_CARDS", "OVER_FOULS"): 0.65,
    ("OVER_CARDS", "OVER_GOALS"): 0.08,  # minimal correlation between cards and goals
    ("OVER_CARDS", "OVER_CORNERS"): 0.05,
    
    ("PLAYER_SHOTS", "PLAYER_SOT"): 0.82,
    ("PLAYER_SOT", "ANYTIME_GOAL"): 0.68,
}


def normalize_market_category(market: str) -> str:
    """Normalize market names to standard categories for correlation lookup."""
    m = market.upper()
    if "GOAL" in m and "OVER" in m:
        return "OVER_GOALS"
    if "GOAL" in m and "UNDER" in m:
        return "UNDER_GOALS"
    if "BTTS" in m or "BOTH_TEAMS" in m:
        return "BTTS_YES" if "YES" in m else "BTTS_NO"
    if "CORNER" in m and "OVER" in m:
        return "OVER_CORNERS"
    if "CORNER" in m and "UNDER" in m:
        return "UNDER_CORNERS"
    if "SOT" in m or "TARGET" in m:
        return "PLAYER_SOT"
    if "SHOT" in m:
        return "PLAYER_SHOTS"
    if "CARD" in m:
        return "OVER_CARDS"
    if "FOUL" in m:
        return "OVER_FOULS"
    if "HOME" in m and "WIN" in m:
        return "HOME_WIN"
    if "AWAY" in m and "WIN" in m:
        return "AWAY_WIN"
    return "GENERIC"


def get_pairwise_correlation(leg_a: dict, leg_b: dict) -> float:
    """
    Returns empirical correlation coefficient between two legs.
    If legs are from different matches, correlation is 0.0.
    """
    if leg_a.get("match_id") != leg_b.get("match_id"):
        return 0.0  # Independent matches
    
    cat_a = normalize_market_category(leg_a.get("market", ""))
    cat_b = normalize_market_category(leg_b.get("market", ""))
    
    if cat_a == cat_b:
        return 0.85 if leg_a.get("player_id") == leg_b.get("player_id") else 0.40
        
    pair_1 = (cat_a, cat_b)
    pair_2 = (cat_b, cat_a)
    
    if pair_1 in MARKET_CORRELATIONS:
        return MARKET_CORRELATIONS[pair_1]
    if pair_2 in MARKET_CORRELATIONS:
        return MARKET_CORRELATIONS[pair_2]
        
    return 0.05  # Slight generic positive intra-match correlation


def build_correlation_matrix(legs: List[dict]) -> np.ndarray:
    """
    Constructs a positive semi-definite correlation matrix for the legs.
    Applies ridge regularisation to ensure Cholesky decomposition validity.
    """
    n = len(legs)
    corr = np.eye(n, dtype=np.float64)
    
    for i in range(n):
        for j in range(i + 1, n):
            rho = get_pairwise_correlation(legs[i], legs[j])
            corr[i, j] = rho
            corr[j, i] = rho
            
    # Regularize to guarantee positive semi-definiteness
    min_eig = np.min(np.real(np.linalg.eigvals(corr)))
    if min_eig < 1e-4:
        corr += (abs(min_eig) + 1e-3) * np.eye(n)
        # Re-normalize diagonal to 1.0
        d = np.sqrt(np.diag(corr))
        corr = corr / np.outer(d, d)
        
    return corr
