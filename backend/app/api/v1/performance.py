from typing import Dict, Any
from fastapi import APIRouter
from app.services.performance_service import performance_service

router = APIRouter(prefix="/performance", tags=["Model Performance & Track Record"])


@router.get("/overview")
async def get_performance_overview() -> Dict[str, Any]:
    """
    Model Performance Center: Historical accuracy, Brier Score, ECE,
    simulated ROI, and calibration diagram data.
    """
    return performance_service.get_performance_overview()
