from typing import Dict, Any, List
from app.models.base import DataStatus


class ConfidenceEngine:
    """
    Computes a composite Confidence Score (0.0 to 1.0) and Risk Warning system.
    Strictly prevents recommendations when fundamental data is missing or stale.
    """
    @staticmethod
    def evaluate_match_data_quality(
        lineup_confirmed: bool,
        matches_sample_size: int,
        data_status: DataStatus,
        has_odds: bool = True
    ) -> Dict[str, Any]:
        warnings = []
        score = 1.0

        if not lineup_confirmed:
            score -= 0.15
            warnings.append("Alineaciones no confirmadas oficialmente; calculadas con titularidad proyectada.")

        if matches_sample_size < 5:
            score -= 0.40
            warnings.append("Muestra histórica insuficiente (<5 partidos). Incertidumbre estadística elevada.")
        elif matches_sample_size < 10:
            score -= 0.15
            warnings.append("Muestra histórica moderada (5-9 partidos).")

        if data_status == DataStatus.STALE:
            score -= 0.25
            warnings.append("Datos desactualizados (>30 minutos sin sincronizar).")
        elif data_status == DataStatus.PROVISIONAL_SYNTHETIC:
            score -= 0.10
            warnings.append("Datos en modo de calibración y simulación local.")

        if not has_odds:
            score -= 0.20
            warnings.append("Sin cuotas de mercado disponibles para verificación de EV.")

        score = max(0.05, min(1.0, score))
        
        is_actionable = score >= 0.60 and matches_sample_size >= 5

        level = "HIGH" if score >= 0.80 else ("MEDIUM" if score >= 0.60 else "LOW")

        return {
            "confidence_score": round(score, 2),
            "confidence_level": level,
            "is_actionable": is_actionable,
            "warnings": warnings
        }
