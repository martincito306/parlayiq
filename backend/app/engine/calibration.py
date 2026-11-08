import numpy as np
from typing import List, Dict, Any, Tuple


class CalibrationEvaluator:
    """
    Evaluates probabilistic model calibration and reliability:
    - Brier Score
    - Log Loss
    - Expected Calibration Error (ECE)
    - Reliability Diagram Bins
    """
    @staticmethod
    def calculate_brier_score(probabilities: List[float], outcomes: List[int]) -> float:
        """
        Brier Score = 1/N * sum((p_i - y_i)^2)
        0.0 is perfect prediction, 0.25 is uninformative coin-flip.
        """
        if not probabilities or len(probabilities) != len(outcomes):
            return 0.25
        p = np.array(probabilities, dtype=np.float64)
        y = np.array(outcomes, dtype=np.float64)
        return float(np.mean((p - y) ** 2))

    @staticmethod
    def calculate_calibration_bins(
        probabilities: List[float],
        outcomes: List[int],
        num_bins: int = 10
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Groups predictions into confidence bins and computes Expected Calibration Error (ECE).
        """
        if not probabilities or len(probabilities) != len(outcomes):
            return [], 0.0

        p = np.array(probabilities, dtype=np.float64)
        y = np.array(outcomes, dtype=np.float64)
        n = len(p)

        bins = np.linspace(0.0, 1.0, num_bins + 1)
        bin_indices = np.digitize(p, bins) - 1

        bin_results = []
        ece = 0.0

        for b in range(num_bins):
            mask = (bin_indices == b)
            count = int(np.sum(mask))
            if count > 0:
                mean_pred = float(np.mean(p[mask]))
                mean_obs = float(np.mean(y[mask]))
                bin_results.append({
                    "bin_center": round((bins[b] + bins[b+1]) / 2.0, 2),
                    "bin_range": f"{round(bins[b], 2)}-{round(bins[b+1], 2)}",
                    "predicted_prob": round(mean_pred, 4),
                    "observed_frequency": round(mean_obs, 4),
                    "count": count
                })
                ece += (count / n) * abs(mean_pred - mean_obs)
            else:
                bin_results.append({
                    "bin_center": round((bins[b] + bins[b+1]) / 2.0, 2),
                    "bin_range": f"{round(bins[b], 2)}-{round(bins[b+1], 2)}",
                    "predicted_prob": round((bins[b] + bins[b+1]) / 2.0, 2),
                    "observed_frequency": 0.0,
                    "count": 0
                })

        return bin_results, round(float(ece), 4)
