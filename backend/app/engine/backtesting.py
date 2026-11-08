import numpy as np
from typing import List, Dict, Any
from app.engine.calibration import CalibrationEvaluator


class HistoricalBacktester:
    """
    Backtesting engine for evaluating prediction track records across seasons.
    Prevents data leakage by strictly using data available before kickoff.
    """
    @staticmethod
    def run_backtest(predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        predictions: list of dicts with:
        - calculated_probability: float
        - market_odds: float
        - outcome: int (1 = won, 0 = lost, -1 = void/push)
        - ev: float
        """
        total = 0
        won = 0
        lost = 0
        void = 0
        
        profit_units = 0.0
        staked_units = 0.0
        
        probs = []
        outcomes = []

        for p in predictions:
            outcome = p.get("outcome", 0)
            odds = p.get("market_odds", 2.0)
            prob = p.get("calculated_probability", 0.5)

            if outcome == -1:
                void += 1
                continue

            total += 1
            staked_units += 1.0
            probs.append(prob)
            outcomes.append(outcome)

            if outcome == 1:
                won += 1
                profit_units += (odds - 1.0)
            else:
                lost += 1
                profit_units -= 1.0

        win_rate = (won / total * 100.0) if total > 0 else 0.0
        roi_pct = (profit_units / staked_units * 100.0) if staked_units > 0 else 0.0
        brier = CalibrationEvaluator.calculate_brier_score(probs, outcomes)
        bins, ece = CalibrationEvaluator.calculate_calibration_bins(probs, outcomes)

        return {
            "total_evaluated": total,
            "won": won,
            "lost": lost,
            "void": void,
            "win_rate_pct": round(win_rate, 2),
            "staked_units": round(staked_units, 2),
            "profit_units": round(profit_units, 2),
            "simulated_roi_pct": round(roi_pct, 2),
            "brier_score": round(brier, 4),
            "expected_calibration_error": round(ece, 4),
            "calibration_bins": bins
        }
