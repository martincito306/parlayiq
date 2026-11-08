import pytest
import numpy as np
from app.engine.poisson_model import DixonColesGoalModel, tau_dixon_coles
from app.engine.negative_binomial import OverdispersedCountModel
from app.engine.player_model import PlayerPropsEngine
from app.engine.correlation_model import build_correlation_matrix, get_pairwise_correlation
from app.engine.monte_carlo import MonteCarloParlaySimulator
from app.engine.parlay_pricing import ParlayPricingEngine
from app.engine.calibration import CalibrationEvaluator


def test_dixon_coles_goal_model():
    model = DixonColesGoalModel(rho=-0.11, max_goals=7)
    res = model.calculate_match_markets(lambda_home=1.8, mu_away=1.2)
    
    assert 0.0 < res["home_win"] < 1.0
    assert 0.0 < res["draw"] < 1.0
    assert 0.0 < res["away_win"] < 1.0
    # Sum of 1X2 must equal approx 1.0
    total_1x2 = res["home_win"] + res["draw"] + res["away_win"]
    assert pytest.approx(total_1x2, abs=0.01) == 1.0
    
    # Over 2.5 + Under 2.5 must equal approx 1.0
    assert pytest.approx(res["over_2_5"] + res["under_2_5"], abs=0.01) == 1.0
    assert len(res["top_exact_scores"]) == 5


def test_negative_binomial_overdispersion():
    # When variance > mean, negative binomial should be used
    mean = 2.4
    var = 4.2
    n, p, is_nbinom = OverdispersedCountModel.fit_parameters(mean, var)
    assert is_nbinom is True
    assert n > 0
    assert 0 < p < 1
    
    res = OverdispersedCountModel.calculate_exceedance_probabilities(mean, var, lines=[0.5, 1.5, 2.5])
    assert res["is_overdispersed"] is True
    assert "over_1.5" in res["lines"]
    assert 0 < res["lines"]["over_1.5"]["probability"] < 1.0


def test_player_props_engine():
    res = PlayerPropsEngine.evaluate_player(
        player_name="Erling Haaland",
        position="FWD",
        shots_per_90=4.1,
        sot_per_90=2.2,
        goals_per_90=0.95,
        fouls_per_90=0.8,
        expected_minutes=85.0,
        is_home=True,
        opponent_conceded_shots_ratio=1.10
    )
    assert res["player_name"] == "Erling Haaland"
    assert res["effective_shots_per_game"] > 3.0
    assert "over_1.5" in res["shots_markets"]
    assert "over_0.5" in res["sot_markets"]
    assert 0.0 < res["anytime_goal"]["probability"] < 1.0


def test_monte_carlo_copula_parlay():
    legs = [
        {"match_id": "M1", "market": "OVER_2.5_GOALS", "individual_probability": 0.58},
        {"match_id": "M1", "market": "PLAYER_SOT", "individual_probability": 0.65},
        {"match_id": "M2", "market": "HOME_WIN", "individual_probability": 0.70}
    ]
    sim = MonteCarloParlaySimulator(num_simulations=10000, seed=123)
    out = sim.simulate_parlay(legs)
    
    assert out["num_simulations"] == 10000
    assert 0.0 < out["joint_probability"] < 1.0
    assert out["fair_odds"] > 1.0
    # SGP legs M1 have positive correlation, so joint prob should differ from independent
    assert "correlation_effect" in out


def test_parlay_pricing_and_ev():
    prob = 0.52
    odds = 2.10
    pricing = ParlayPricingEngine.evaluate_pricing(prob, odds)
    
    # EV = 0.52 * 2.10 - 1 = 1.092 - 1 = +0.092 (+9.2% positive value)
    assert pricing["expected_value"] > 0
    assert pricing["is_positive_value"] is True
    assert pricing["fair_odds"] == round(1.0 / 0.52, 2)
    assert pricing["edge_percentage"] > 0


def test_calibration_evaluator():
    probs = [0.9, 0.8, 0.7, 0.2, 0.1]
    outcomes = [1, 1, 1, 0, 0]
    brier = CalibrationEvaluator.calculate_brier_score(probs, outcomes)
    assert brier < 0.10  # Well calibrated predictions have low brier score
    
    bins, ece = CalibrationEvaluator.calculate_calibration_bins(probs, outcomes, num_bins=5)
    assert len(bins) == 5
    assert 0.0 <= ece <= 1.0
