import numpy as np
from scipy.stats import poisson
from typing import Dict, Tuple, Any


def tau_dixon_coles(x: int, y: int, lambda_param: float, mu_param: float, rho: float = -0.11) -> float:
    """
    Dixon-Coles correction factor for low-scoring match outcomes.
    Corrects standard bivariate Poisson independence flaw for 0-0, 1-0, 0-1, 1-1.
    """
    if x == 0 and y == 0:
        return 1.0 - (lambda_param * mu_param * rho)
    elif x == 0 and y == 1:
        return 1.0 + (lambda_param * rho)
    elif x == 1 and y == 0:
        return 1.0 + (mu_param * rho)
    elif x == 1 and y == 1:
        return 1.0 - rho
    else:
        return 1.0


class DixonColesGoalModel:
    """
    Bivariate Dixon-Coles Poisson model for soccer match outcomes.
    Computes exact scoreline probability matrix and all derivative goal markets.
    """
    def __init__(self, rho: float = -0.11, max_goals: int = 7):
        self.rho = rho
        self.max_goals = max_goals

    def compute_score_matrix(self, lambda_home: float, mu_away: float) -> np.ndarray:
        """
        Calculates matrix P(home_goals = i, away_goals = j) for i, j in [0, max_goals].
        """
        matrix = np.zeros((self.max_goals + 1, self.max_goals + 1), dtype=np.float64)
        for i in range(self.max_goals + 1):
            p_home = poisson.pmf(i, lambda_home)
            for j in range(self.max_goals + 1):
                p_away = poisson.pmf(j, mu_away)
                correction = tau_dixon_coles(i, j, lambda_home, mu_away, self.rho)
                matrix[i, j] = p_home * p_away * max(0.0, correction)
        
        # Normalize matrix so total sum is 1.0
        total_p = np.sum(matrix)
        if total_p > 0:
            matrix /= total_p
        return matrix

    def calculate_match_markets(self, lambda_home: float, mu_away: float) -> Dict[str, Any]:
        """
        Derives all 1X2, Over/Under, BTTS, and Exact Score probabilities.
        """
        matrix = self.compute_score_matrix(lambda_home, mu_away)
        
        # 1X2 probabilities
        home_win_p = float(np.sum(np.tril(matrix, -1)))
        draw_p = float(np.sum(np.diag(matrix)))
        away_win_p = float(np.sum(np.triu(matrix, 1)))
        
        # Over / Under Goals
        total_goals_grid = np.fromfunction(lambda i, j: i + j, (self.max_goals + 1, self.max_goals + 1), dtype=int)
        
        over_0_5 = float(np.sum(matrix[total_goals_grid > 0.5]))
        over_1_5 = float(np.sum(matrix[total_goals_grid > 1.5]))
        over_2_5 = float(np.sum(matrix[total_goals_grid > 2.5]))
        over_3_5 = float(np.sum(matrix[total_goals_grid > 3.5]))
        
        under_1_5 = 1.0 - over_1_5
        under_2_5 = 1.0 - over_2_5
        under_3_5 = 1.0 - over_3_5
        
        # Both Teams To Score (BTTS)
        btts_yes = float(np.sum(matrix[1:, 1:]))
        btts_no = 1.0 - btts_yes
        
        # Double Chance
        dc_1x = home_win_p + draw_p
        dc_x2 = draw_p + away_win_p
        dc_12 = home_win_p + away_win_p
        
        # Top 5 Most Probable Exact Scores
        flat_indices = np.argsort(matrix.ravel())[::-1][:5]
        top_scores = []
        for idx in flat_indices:
            h = int(idx // (self.max_goals + 1))
            a = int(idx % (self.max_goals + 1))
            prob = float(matrix[h, a])
            top_scores.append({"score": f"{h}-{a}", "probability": prob, "fair_odds": round(1.0 / max(0.0001, prob), 2)})
            
        return {
            "lambda_home": round(lambda_home, 3),
            "mu_away": round(mu_away, 3),
            "home_win": round(home_win_p, 4),
            "draw": round(draw_p, 4),
            "away_win": round(away_win_p, 4),
            "over_1_5": round(over_1_5, 4),
            "under_1_5": round(under_1_5, 4),
            "over_2_5": round(over_2_5, 4),
            "under_2_5": round(under_2_5, 4),
            "over_3_5": round(over_3_5, 4),
            "under_3_5": round(under_3_5, 4),
            "btts_yes": round(btts_yes, 4),
            "btts_no": round(btts_no, 4),
            "double_chance_1x": round(dc_1x, 4),
            "double_chance_x2": round(dc_x2, 4),
            "top_exact_scores": top_scores,
            "matrix": matrix.tolist()
        }
