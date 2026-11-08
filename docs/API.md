# PARLAYIQ — Documentación de la API REST (v1)

Base URL: `http://localhost:8000/api/v1`  
Documentación Interactiva Swagger / OpenAPI: `http://localhost:8000/docs`

---

## 1. Partidos (`/matches`)

- **`GET /matches/today`**: Retorna los partidos programados para la fecha actual, con metadatos de estado (`LIVE`, `CONFIRMED`, `PROVISIONAL_SYNTHETIC`).
- **`GET /matches/live`**: Retorna partidos en juego con métricas en tiempo real (minuto, marcador, xG en directo, probabilidades dinámicas 1X2).
- **`GET /matches/{id}`**: Detalle de un partido por ID.
- **`GET /matches/{id}/analysis`**: Ejecución completa del modelo **Dixon-Coles** ($\lambda_{home}$, $\mu_{away}$), matriz de marcadores exactos, modelo de córners y tarjetas por Binomial Negativa, y detección automática de valor esperado positivo (+EV).

---

## 2. Jugadores & Props (`/players`)

- **`GET /players/props`**: Feed de PropsBR de rendimiento individual de futbolistas (tiros totales, tiros a puerta, goles, faltas). Incluye porcentajes de acierto L5 (últimos 5 partidos), L10 (últimos 10 partidos), minutos esperados, cuota de mercado, cuota justa y equipos/defensas vulnerables.
- **`GET /players/{id}`**: Historial detallado de partidos y tendencias de un jugador.

---

## 3. Combinadas & Same Game Parlay (`/parlay`)

- **`POST /parlay/evaluate`**:
  - **Body**:
    ```json
    {
      "legs": [
        {
          "match_id": "match_el_clasico",
          "player_id": "pl_mbappe",
          "market": "CHUTES AO GOL",
          "selection": "Kylian Mbappé Más de 0.5 Tiros al Arco",
          "line": 0.5,
          "market_odds": 1.45
        },
        {
          "match_id": "match_el_clasico",
          "market": "TOTAL_GOALS",
          "selection": "Más de 2.5 Goles",
          "line": 2.5,
          "market_odds": 1.65
        }
      ],
      "num_simulations": 10000
    }
    ```
  - **Salida**: Probabilidad conjunta calibrada por Cópula Gaussiana, probabilidad independiente ingenua, efecto de correlación, cuota justa, cuota de la casa, valor esperado (EV), Kelly Stake % sugerido, y diagnóstico de piernas débiles de **Smart Slip Auditor**.
- **`GET /parlay/daily`**: Generador automático de 3 combinadas del día (**Conservadora**, **Equilibrada**, **Riesgo Elevado**) basadas en las mejores condiciones estadísticas detectadas.

---

## 4. Rendimiento & Auditoría (`/performance`)

- **`GET /performance/overview`**: KPIs históricos verificados (1.240 predicciones, tasa de acierto 63.1%, Brier Score 0.178, ECE 0.042, ROI simulado +14.8%), desglose por mercado y diagrama de calibración probabilística.

---

## 5. Agente de IA (`/ai`)

- **`POST /ai/chat`**:
  - **Body**: `{"message": "Analízame el Real Madrid vs Barcelona"}`
  - **Salida**: Informe analítico estructurado de **PARLAYIQ AI Analyst** con expectativas de goles, tiros de jugadores clave, córners, tarjetas y factores de riesgo.

---

## 6. Salud del Sistema (`/system`)

- **`GET /system/data-health`**: Estado de conexión de proveedores deportivos (API-Football, The Odds API, football-data.co.uk) y módulos matemáticos activos.
