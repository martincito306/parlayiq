import sys
import os
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from tests.test_quantitative_engine import (
    test_dixon_coles_goal_model,
    test_negative_binomial_overdispersion,
    test_player_props_engine,
    test_monte_carlo_copula_parlay,
    test_parlay_pricing_and_ev,
    test_calibration_evaluator
)

from tests.test_api_endpoints import (
    test_api_root_and_health,
    test_calendar_and_radar_endpoints,
    test_players_props_endpoint,
    test_parlays_sgp_vs_multipartido,
    test_ai_analyst_chat
)

async def main():
    print("==================================================")
    print("PARLAYIQ V2 — COMPREHENSIVE AUTOMATED TEST SUITE")
    print("==================================================")

    print("\n--- FASE 4: MOTOR MATEMÁTICO CUANTITATIVO ---")
    test_dixon_coles_goal_model()
    print(" [x] PASS: Dixon-Coles Goal Model & 1X2 Probabilities")

    test_negative_binomial_overdispersion()
    print(" [x] PASS: Negative Binomial Overdispersion & Threshold Probabilities")

    test_player_props_engine()
    print(" [x] PASS: Player Props Engine (Haaland Shots, SOT, Expected Minutes)")

    test_monte_carlo_copula_parlay()
    print(" [x] PASS: Monte Carlo 10,000 vectorised simulations & Gaussian Copula")

    test_parlay_pricing_and_ev()
    print(" [x] PASS: Parlay Pricing, Fair Odds, and Expected Value (EV)")

    test_calibration_evaluator()
    print(" [x] PASS: Calibration Evaluator (Brier Score & ECE)")

    print("\n--- FASE 2, 6, 8, 10: ENDPOINTS Y LÓGICA V2 INTEGRADA ---")
    await test_api_root_and_health()
    print(" [x] PASS: API Root & Data Health Audit")

    await test_calendar_and_radar_endpoints()
    print(" [x] PASS: Calendario Dinámico (America/Bogota) & PARLAYIQ RADAR")

    await test_players_props_endpoint()
    print(" [x] PASS: Player Intelligence 2.0 (100% Español, L5/L10/L20)")

    await test_parlays_sgp_vs_multipartido()
    print(" [x] PASS: Distinción Matemática SGP (Mismo Partido) vs Combinada Multipartido")

    await test_ai_analyst_chat()
    print(" [x] PASS: PARLAYIQ AI Analyst 2.0 (Intelligence Engine)")

    print("\n==================================================")
    print(" ALL 11 TEST SUITES PASSED WITH 100% SUCCESS!")
    print("==================================================")

if __name__ == "__main__":
    try:
        asyncio.run(main())
        sys.exit(0)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\nFAILED with error: {e}")
        sys.exit(1)
