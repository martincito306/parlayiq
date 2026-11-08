from typing import List, Dict
from pydantic import BaseModel


class CalibrationBin(BaseModel):
    bin_center: float
    predicted_prob: float
    observed_frequency: float
    count: int


class ModelPerformanceOverview(BaseModel):
    total_predictions: int
    settled_predictions: int
    won_predictions: int
    lost_predictions: int
    win_rate: float
    brier_score: float
    expected_calibration_error: float
    simulated_roi_pct: float
    profit_units: float
    closing_line_value_avg_pct: float
    calibration_curve: List[CalibrationBin]
    by_market: Dict[str, Dict[str, float]]
    historical_trend: List[Dict[str, float]]
