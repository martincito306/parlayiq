import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_api_root_and_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ONLINE"
        assert data["name"] == "PARLAYIQ API"

        r_health = await ac.get("/api/v1/system/data-health")
        assert r_health.status_code == 200
        health = r_health.json()
        assert health["status"] == "HEALTHY"
        assert "quant_engine" in health


@pytest.mark.asyncio
async def test_calendar_and_radar_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Calendar endpoint (America/Bogota)
        r_cal = await ac.get("/api/v1/matches/calendar")
        assert r_cal.status_code == 200
        cal = r_cal.json()
        assert "current_colombian_date" in cal
        assert "timezone" in cal
        assert cal["total_matches"] > 0
        assert "matches" in cal

        # Radar endpoint
        r_radar = await ac.get("/api/v1/matches/radar")
        assert r_radar.status_code == 200
        radar = r_radar.json()
        assert "mercados" in radar
        assert "disparos_a_puerta" in radar["mercados"]


@pytest.mark.asyncio
async def test_players_props_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/api/v1/players/props")
        assert r.status_code == 200
        props = r.json()
        assert len(props) > 0
        first_prop = props[0]
        assert "player_name" in first_prop
        assert "l5_pct" in first_prop
        assert "l10_pct" in first_prop
        assert "confidence_pct" in first_prop
        assert first_prop["market"] in ["DISPAROS", "DISPAROS A PUERTA"]


@pytest.mark.asyncio
async def test_parlays_sgp_vs_multipartido():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Test Same Game Parlay (same match_id)
        sgp_payload = {
            "legs": [
                {
                    "match_id": "match_el_clasico",
                    "player_id": "pl_mbappe",
                    "market": "DISPAROS_A_PUERTA",
                    "selection": "Kylian Mbappé Más de 0.5 Disparos a Puerta",
                    "line": 0.5,
                    "market_odds": 1.45
                },
                {
                    "match_id": "match_el_clasico",
                    "market": "TOTAL_GOLES",
                    "selection": "Más de 2.5 Goles",
                    "line": 2.5,
                    "market_odds": 1.65
                }
            ],
            "num_simulations": 10000
        }
        r_sgp = await ac.post("/api/v1/parlay/evaluate", json=sgp_payload)
        assert r_sgp.status_code == 200
        sgp_data = r_sgp.json()
        assert sgp_data["is_same_game_parlay"] is True
        assert sgp_data["parlay_type"] == "SAME_GAME_PARLAY"

        # 2. Test Combinada Multipartido (different match_ids)
        multi_payload = {
            "legs": [
                {
                    "match_id": "match_el_clasico",
                    "market": "TOTAL_GOLES",
                    "selection": "Más de 2.5 Goles",
                    "line": 2.5,
                    "market_odds": 1.65
                },
                {
                    "match_id": "match_pl_title",
                    "market": "1X2",
                    "selection": "Victoria Manchester City",
                    "market_odds": 1.35
                }
            ],
            "num_simulations": 10000
        }
        r_multi = await ac.post("/api/v1/parlay/evaluate", json=multi_payload)
        assert r_multi.status_code == 200
        multi_data = r_multi.json()
        assert multi_data["is_same_game_parlay"] is False
        assert multi_data["parlay_type"] == "COMBINADA_MULTIPARTIDO"


@pytest.mark.asyncio
async def test_ai_analyst_chat():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r_ai = await ac.post("/api/v1/ai/chat", json={"message": "¿Cuáles son las oportunidades del radar hoy?"})
        assert r_ai.status_code == 200
        ai_resp = r_ai.json()
        assert "reply" in ai_resp
        assert "PARLAYIQ RADAR" in ai_resp["reply"]
