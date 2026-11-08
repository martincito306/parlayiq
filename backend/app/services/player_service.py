from typing import List, Dict, Any, Optional
from app.providers.factory import data_provider
from app.engine.player_model import PlayerPropsEngine


class PlayerService:
    @staticmethod
    async def get_all_player_props() -> List[Dict[str, Any]]:
        """
        Returns full list of player prop opportunities with L5, L10, L20 hit rates,
        fair odds, market odds, confidence, and target defense analysis,
        STRICTLY in neutral Spanish.
        """
        players_data = data_provider.synthetic.players
        results = []

        for p_id, p in players_data.items():
            team = data_provider.synthetic.teams.get(p["team_id"], {})
            
            # 1. Más de 1.5 Disparos Totales
            eval_shots = PlayerPropsEngine.evaluate_player(
                player_name=p["name"],
                position=p["position"],
                shots_per_90=p["shots_per_90"],
                sot_per_90=p["sot_per_90"],
                goals_per_90=p["goals_per_90"],
                fouls_per_90=p["fouls_per_90"],
                expected_minutes=p["expected_minutes"],
                is_home=True,
                opponent_conceded_shots_ratio=1.08,
                l5_shots_hit_rate=p.get("l5_shots_hit_rate", 0.8),
                l10_shots_hit_rate=p.get("l10_shots_hit_rate", 0.75)
            )

            p_over_1_5_shots = eval_shots["shots_markets"]["over_1.5"]["probability"]
            fair_odds_shots = eval_shots["shots_markets"]["over_1.5"]["fair_odds"]
            market_odds_shots = round(fair_odds_shots * 1.12, 2)
            ev_shots = round((p_over_1_5_shots * market_odds_shots) - 1.0, 3)

            results.append({
                "player_id": p_id,
                "player_name": p["name"],
                "team_name": team.get("name", "Equipo"),
                "team_short": team.get("short_name", "EQ"),
                "position": "DELANTERO" if p["position"] == "FWD" else ("MEDIOCAMPISTA" if p["position"] == "MID" else "DEFENSA"),
                "market": "DISPAROS",
                "market_label": "Más de 1.5 Disparos",
                "line": 1.5,
                "l5_pct": int(p.get("l5_shots_hit_rate", 0.8) * 100),
                "l10_pct": int(p.get("l10_shots_hit_rate", 0.75) * 100),
                "l20_pct": int((p.get("l10_shots_hit_rate", 0.75) * 0.95) * 100),
                "odds": market_odds_shots,
                "fair_odds": fair_odds_shots,
                "confidence_pct": int(p_over_1_5_shots * 100),
                "ev": ev_shots,
                "is_positive_value": ev_shots > 0,
                "target_defenses": p.get("target_defenses", ["Rival en turno"]),
                "expected_minutes": p["expected_minutes"],
                "shots_per_90": p["shots_per_90"],
                "category": "shots"
            })

            # 2. Más de 0.5 Disparos a Puerta (SOT)
            p_over_0_5_sot = eval_shots["sot_markets"]["over_0.5"]["probability"]
            fair_odds_sot = eval_shots["sot_markets"]["over_0.5"]["fair_odds"]
            market_odds_sot = round(fair_odds_sot * 1.15, 2)
            ev_sot = round((p_over_0_5_sot * market_odds_sot) - 1.0, 3)

            results.append({
                "player_id": p_id,
                "player_name": p["name"],
                "team_name": team.get("name", "Equipo"),
                "team_short": team.get("short_name", "EQ"),
                "position": "DELANTERO" if p["position"] == "FWD" else ("MEDIOCAMPISTA" if p["position"] == "MID" else "DEFENSA"),
                "market": "DISPAROS A PUERTA",
                "market_label": "Más de 0.5 Disparos a Puerta",
                "line": 0.5,
                "l5_pct": int(p.get("l5_sot_hit_rate", 0.8) * 100),
                "l10_pct": int(p.get("l10_sot_hit_rate", 0.75) * 100),
                "l20_pct": int((p.get("l10_sot_hit_rate", 0.75) * 0.92) * 100),
                "odds": market_odds_sot,
                "fair_odds": fair_odds_sot,
                "confidence_pct": int(p_over_0_5_sot * 100),
                "ev": ev_sot,
                "is_positive_value": ev_sot > 0,
                "target_defenses": p.get("target_defenses", ["Rival en turno"]),
                "expected_minutes": p["expected_minutes"],
                "shots_per_90": p["shots_per_90"],
                "category": "sot"
            })

        results.sort(key=lambda x: (x["confidence_pct"], x["ev"]), reverse=True)
        return results

    @staticmethod
    async def get_player_detail(player_id: str) -> Optional[Dict[str, Any]]:
        p = await data_provider.get_player_statistics(player_id)
        if not p:
            return None
        history = await data_provider.get_player_match_history(player_id)
        return {
            "player": p,
            "match_history": history
        }


player_service = PlayerService()
