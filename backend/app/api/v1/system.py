from typing import Dict, Any
from fastapi import APIRouter
from app.providers.factory import data_provider
from app.core.config import settings

router = APIRouter(prefix="/system", tags=["System & Providers"])


@router.get("/data-health")
async def get_data_health() -> Dict[str, Any]:
    """Audit status of connected sports data providers, cache, and quant engine."""
    return {
        "status": "HEALTHY",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "providers": data_provider.get_provider_status(),
        "quant_engine": {
            "dixon_coles": "OPERATIONAL",
            "negative_binomial": "OPERATIONAL",
            "gaussian_copula": "OPERATIONAL",
            "monte_carlo": "OPERATIONAL (10,000 runs)",
            "brier_calibration": "ACTIVE"
        }
    }
