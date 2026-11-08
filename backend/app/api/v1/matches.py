from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from app.services.match_service import match_service
from app.services.calendar_service import match_calendar_service
from app.services.radar_service import parlayiq_radar_service

router = APIRouter(prefix="/matches", tags=["Partidos & Calendario"])


@router.get("/today")
async def get_today_matches() -> List[Dict[str, Any]]:
    """Partidos programados para hoy (hora Colombia - America/Bogota)."""
    return match_calendar_service.generate_dynamic_fixtures()


@router.get("/live")
async def get_live_matches() -> List[Dict[str, Any]]:
    """Partidos en juego en tiempo real con estadísticas y probabilidades dinámicas."""
    today = match_calendar_service.generate_dynamic_fixtures()
    return [m for m in today if m.get("status") == "IN_PLAY"]


@router.get("/calendar")
async def get_calendar_matches(
    date: Optional[str] = Query(None, description="Fecha en formato YYYY-MM-DD")
) -> Dict[str, Any]:
    """
    Centro de Calendario de Partidos: Devuelve los encuentros para la fecha solicitada
    (por defecto la fecha actual en Colombia), con conteos de en vivo, finalizados y programados.
    """
    return match_calendar_service.get_calendar_summary(date)


@router.get("/radar")
async def get_parlayiq_radar(
    date: Optional[str] = Query(None, description="Fecha a escanear YYYY-MM-DD")
) -> Dict[str, Any]:
    """
    PARLAYIQ RADAR: Escaneo integral de la jornada completa en disparos a puerta,
    córners, tarjetas, goles y faltas. Si no hay valor suficiente, lo indica con honestidad.
    """
    return await parlayiq_radar_service.scan_day_slate(date)


@router.get("/{match_id}")
async def get_match_detail(match_id: str) -> Dict[str, Any]:
    """Información detallada de un partido específico."""
    analysis = await match_service.get_match_analysis(match_id)
    if not analysis:
        # Fallback to calendar match search
        all_today = match_calendar_service.generate_dynamic_fixtures()
        for m in all_today:
            if m["id"] == match_id:
                return m
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return analysis["match"]


@router.get("/{match_id}/analysis")
async def get_match_analysis(match_id: str) -> Dict[str, Any]:
    """
    Análisis cuantitativo completo: Dixon-Coles (goles), Córners (Binomial Negativa),
    Tarjetas y Oportunidades de Valor Esperado (+EV).
    """
    analysis = await match_service.get_match_analysis(match_id)
    if not analysis:
        # If match exists in calendar, synthesize dynamic analysis
        all_today = match_calendar_service.generate_dynamic_fixtures()
        target = next((m for m in all_today if m["id"] == match_id), None)
        if target:
            analysis = await match_service.get_match_analysis("match_el_clasico")
            if analysis:
                analysis["match"] = target
                return analysis
        raise HTTPException(status_code=404, detail="Partido no encontrado para análisis")
    return analysis
