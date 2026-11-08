from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from app.services.player_service import player_service

router = APIRouter(prefix="/players", tags=["Players & Props"])


@router.get("/props")
async def get_player_props() -> List[Dict[str, Any]]:
    """
    Retrieve all player prop opportunities (Shots, Shots on Target, Goals, Fouls)
    with L5%, L10%, Expected Minutes, Odds, AI Confidence %, and Target Defenses.
    """
    return await player_service.get_all_player_props()


@router.get("/{player_id}")
async def get_player_details(player_id: str) -> Dict[str, Any]:
    """Retrieve detailed player statistics and recent match logs."""
    detail = await player_service.get_player_detail(player_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Player not found")
    return detail
