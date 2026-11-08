import numpy as np
from scipy.stats import norm
from typing import List, Dict, Any
from app.engine.correlation_model import build_correlation_matrix


class MonteCarloParlaySimulator:
    """
    Vectorized Monte Carlo simulation engine for parlays and Same Game Parlays (SGP).
    Uses Gaussian Copula to properly model inter-event dependencies.
    """
    def __init__(self, num_simulations: int = 10000, seed: int = 42):
        self.num_simulations = max(1000, min(100000, num_simulations))
        self.rng = np.random.default_rng(seed)

    def simulate_parlay(self, legs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Simulates joint occurrence of legs.
        Each leg dict must contain:
        - individual_probability: float in (0, 1)
        - market: str
        - match_id: str
        """
        n_legs = len(legs)
        if n_legs == 0:
            return {"joint_probability": 0.0, "fair_odds": 1.0, "num_simulations": self.num_simulations}
            
        if n_legs == 1:
            p = float(legs[0].get("individual_probability", 0.5))
            return {
                "joint_probability": round(p, 4),
                "independent_probability": round(p, 4),
                "correlation_effect": 0.0,
                "fair_odds": round(1.0 / max(0.0001, p), 2),
                "num_simulations": self.num_simulations,
                "std_error": 0.0
            }

        # 1. Marginal probabilities
        marginal_probs = np.array([float(leg.get("individual_probability", 0.5)) for leg in legs])
        # Naive independent probability (for comparison)
        independent_prob = float(np.prod(marginal_probs))

        # 2. Build correlation matrix
        corr_matrix = build_correlation_matrix(legs)

        # 3. Cholesky decomposition of correlation matrix
        try:
            L = np.linalg.cholesky(corr_matrix)
        except np.linalg.LinAlgError:
            # Fallback to nearest positive definite if needed
            eigval, eigvec = np.linalg.eigh(corr_matrix)
            eigval = np.maximum(eigval, 1e-4)
            reconstructed = eigvec @ np.diag(eigval) @ eigvec.T
            L = np.linalg.cholesky(reconstructed)

        # 4. Generate independent standard normal draws: shape (num_simulations, n_legs)
        Z_ind = self.rng.standard_normal((self.num_simulations, n_legs))
        
        # 5. Correlate draws: Z_corr = Z_ind @ L.T
        Z_corr = Z_ind @ L.T
        
        # 6. Transform to uniform marginals via standard normal CDF: U = Phi(Z_corr)
        U = norm.cdf(Z_corr)
        
        # 7. Check if each simulated leg hits its marginal threshold: U_i <= p_i
        hits_matrix = (U <= marginal_probs)
        
        # 8. All legs hit in same simulation run
        parlay_hits = np.all(hits_matrix, axis=1)
        success_count = int(np.sum(parlay_hits))
        joint_prob = float(success_count / self.num_simulations)
        
        # Standard error of Monte Carlo estimator: sqrt(p * (1 - p) / N)
        std_error = float(np.sqrt(max(0.0, joint_prob * (1.0 - joint_prob) / self.num_simulations)))
        
        # Bound joint probability between valid limits
        joint_prob = max(1e-4, min(0.9999, joint_prob))
        fair_odds = round(1.0 / joint_prob, 2)
        correlation_effect = round(joint_prob - independent_prob, 4)

        return {
            "joint_probability": round(joint_prob, 4),
            "independent_probability": round(independent_prob, 4),
            "correlation_effect": correlation_effect,
            "fair_odds": fair_odds,
            "num_simulations": self.num_simulations,
            "std_error": round(std_error, 4),
            "correlation_matrix": corr_matrix.tolist()
        }
