from typing import Dict, Any
from fastapi import APIRouter
from app.schemas.ai import AIChatRequest
from app.agents.parlayiq_agent import parlayiq_agent

router = APIRouter(prefix="/ai", tags=["PARLAYIQ AI Analyst"])


@router.post("/chat")
async def ai_chat(request: AIChatRequest) -> Dict[str, Any]:
    """
    PARLAYIQ INTELLIGENCE ENGINE 2.0:
    Consulta autónoma conectada con el calendario dinámico de Colombia,
    escaneo RADAR de la jornada completa y modelos matemáticos.
    """
    return await parlayiq_agent.execute_analyst_task(
        message=request.message,
        match_id=request.match_id
    )
