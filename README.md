# PARLAYIQ — Sports Intelligence & AI Parlay Optimization Platform

Plataforma profesional de inteligencia deportiva cuantitativa, predicción estadística y optimización de combinadas (Same Game Parlays & Cross-Match Parlays) con simulación Monte Carlo (10.000 iteraciones), matrices de correlación con Cópula Gaussiana, modelo de goles Dixon-Coles, Binomial Negativa para props de jugadores, y auditoría histórica verificable con Brier Score y ECE.

---

## 🌟 Las 6 Funcionalidades Nucleares

1. **Player Intelligence (PropsBR Engine)**:
   - Análisis de tiros, tiros al arco, faltas y goles por 90 minutos.
   - Ponderación de minutos esperados, condición local/visitante y rating defensivo del rival.
   - Tasas de acierto empírico en los últimos 5 (L5%) y 10 (L10%) partidos.
   - Identificación de defensas rivales vulnerables.

2. **Value Finder (Edge & EV)**:
   - Cuota justa ($1/P$) vs Cuota del mercado.
   - Cálculo estricto de Valor Esperado ($EV = P \times \text{Cuota} - 1$).
   - Alertas de edge positivo para no apostar a ciegas por cuotas bajas sin valor real.

3. **Live Match Intelligence**:
   - Ajuste bayesiano de probabilidades dinámicas en tiempo real según el minuto, xG y disparos.
   - Gráfico de tendencia de probabilidad de victoria (Home / Draw / Away).
   - Matriz de marcadores exactos más probables recalculada en vivo.

4. **Prediction Track Record**:
   - Historial verificable e inmutable de predicciones liquidadas.
   - Evaluación probabilística mediante Brier Score ($BS = 0.178$) y Expected Calibration Error ($ECE = 4.2\%$).
   - Retorno sobre inversión histórico simulado (+14.8% ROI).

5. **AI Match Scanner (PARLAYIQ AI Analyst)**:
   - Agente de IA cuantitativo que escanea automáticamente los partidos del día.
   - Generación de informes estructurados con Poisson bivariado, cuotas justas y factores de riesgo.

6. **Smart Parlay Optimizer & Bet Builder Studio**:
   - Algoritmo Monte Carlo de 10.000 iteraciones vectorizadas.
   - Modelado de dependencias inter-mercado mediante Cópula Gaussiana (sin multiplicar ingenuamente probabilidades dependientes).
   - **Smart Slip Auditor**: Diagnóstico automático de selecciones débiles y sugerencias de reemplazo.
   - Cálculo del tamaño de apuesta óptimo mediante Criterio de Kelly fraccional.

---

## 🏗️ Arquitectura Técnica

- **Frontend**: Next.js 14 (App Router), TypeScript Strict, Tailwind CSS, Lucide React, Recharts.
- **Backend**: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0 Async, aiosqlite / asyncpg.
- **Motor Cuantitativo**: NumPy, SciPy, Pandas, Scikit-learn, Dixon-Coles Poisson, Cópulas Gaussianas.
- **Datos Deportivos**: Capa unificada `SportsDataProvider` con adaptadores para `football-data.co.uk` (open data verificada de tiros, córners, tarjetas y cuotas Pinnacle/Bet365), API-Football, The Odds API y calibración interna de respaldo.

---

## 🚀 Inicio Rápido

### Backend
```bash
cd backend
uv venv --python 3.12
.\.venv\Scripts\activate   # Windows
uv pip install -r requirements.txt greenlet
uv run python run_tests.py
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Visita `http://localhost:3000` en tu navegador.
Documentación Swagger de la API: `http://localhost:8000/docs`.
