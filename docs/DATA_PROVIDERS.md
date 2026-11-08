# PARLAYIQ — Auditoría y Estrategia de Proveedores de Datos Deportivos

Este documento establece la auditoría técnica de fuentes de datos de fútbol para **PARLAYIQ**, analizando costos, coberturas de mercados (goles, tiros de jugadores, córners, tarjetas, cuotas en vivo), límites de API y la arquitectura unificada de adaptadores.

---

## 1. Matriz Comparativa de Proveedores

| Proveedor | Datos Gratuitos / Tier Gratuito | Estadísticas de Jugadores (Tiros, Faltas, Pases) | Cuotas de Apuestas (Odds) | Datos en Directo (Live) | Requiere Suscripción Paga para Producción | Latencia / Límites |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **football-data.co.uk** | 100% Gratuito (Open Data CSV) | Por partido/equipo (Tiros, Tiros al arco, Faltas, Córners, Tarjetas) | Sí (Pinnacle, Bet365, BetFair, BWin, etc.) | No (Post-partido & histórico) | **NO** (Dominio público, actualización diaria/semanal) | Sin límites. Ideal para backtesting y calibración cuantitativa (Poisson, Dixon-Coles). |
| **API-Football (api-sports.io)** | 100 req/día gratis | Sí (Tiros al arco, faltas, asistencias, pases, minutos, calificaciones) | Sí (Pre-partido y en vivo en planes Pro) | Sí (Marcadores, eventos, alineaciones) | Sí para alto tráfico (Gratis: 100 req/día; Pro: 29€/mes) | Latencia ~300ms. Excelente balance calidad/precio. |
| **football-data.org** | 10 req/min gratis | Básicas (goleadores, alineaciones básicas) | Limitadas | Sí (Marcador en vivo, 12 ligas top) | Sí para ligas secundarias | Muy estable, excelente para calendarios y resultados oficiales. |
| **The Odds API** | 500 req/mes gratis | No (enfocado en cuotas de casas) | Sí (Bet365, Pinnacle, Bovada, DraftKings, 1X2, Totales, Spreads) | Sí (Cuotas actualizadas cada 5-15 min) | Sí para cuotas de jugadores props (Gratis: 500 req/mes; $30+/mes) | Baja latencia, cuotas reales de múltiples casas. |
| **SofaScore / FotMob (Scraping / Endpoints Públicos)** | Gratuito mediante scraping ético / proxies | Muy detalladas (Mapas de calor, mapas de tiros, xG, duelos, faltas, L5/L10) | Sí (Cuotas de apertura y actuales) | Sí (Eventos en tiempo real, momentum, posesión) | **NO** (Uso de rotación de headers y parsers JSON) | Requiere rate limiting defensivo y caching en Redis para evitar bloqueos. |
| **Opta / StatsBomb / Sportradar** | No (Enterprise B2B) | Máximo nivel (coordenadas x,y de pases, presiones, tracking 25 FPS) | Sí en feeds de apuestas | Sí (Ultra baja latencia <1s) | **SÍ** ($1.000 - $15.000+ USD/mes) | Fuera de presupuesto para etapa inicial / MVP. |

---

## 2. Estrategia "Zero-Budget" y Comercialización Inicial

Para permitir que PARLAYIQ funcione de inmediato sin presupuesto inicial pero con calidad profesional y datos comprobables:

1. **Backtesting & Calibración de Modelos Cuantitativos**:
   - Integración nativa con `football-data.co.uk` para 5 grandes ligas europeas (Premier League, La Liga, Serie A, Bundesliga, Ligue 1) + Champions League.
   - Proporciona más de 20 años de datos verificados de tiros, córners, tarjetas y cuotas reales de Pinnacle y Bet365 para calibrar Poisson, Binomial Negativa y Dixon-Coles.

2. **Partidos de Hoy, Alineaciones y Estadísticas en Vivo**:
   - **Adaptador Híbrido**: Consultas a endpoints públicos y API-Football (en modo tier gratuito con caché de 15 minutos en Redis/memoria).
   - Extracción de datos de partidos de hoy, minutos jugados y rendimiento reciente (L5, L10) de jugadores.

3. **Capa Unificada `SportsDataProvider`**:
   - Todos los servicios de la plataforma interactúan **únicamente** con la interfaz abstracta `SportsDataProvider`.
   - Se configuran adaptadores intercambiables:
     - `FootballDataCoUkProvider`
     - `ApiFootballProvider`
     - `TheOddsApiProvider`
     - `PublicWebProvider`
     - `SyntheticFixtureProvider` (identificado inequívocamente con status `PROVISIONAL_SYNTHETIC`).
   - Cuando el usuario adquiera una API Key comercial de API-Football o Sportmonks, basta con configurarla en `.env` sin modificar una sola línea del motor matemático ni del frontend.

---

## 3. Estados de Integridad y Trazabilidad de Datos

Cada registro devuelto por cualquier proveedor lleva metadata obligatoria:

```json
{
  "source": "football-data.co.uk",
  "updated_at": "2026-11-08T14:00:00Z",
  "event_time": "2026-11-08T18:00:00Z",
  "provider_id": "PL_2025_M30",
  "confidence_score": 0.95,
  "status": "CONFIRMED"
}
```

Estados válidos:
- **`LIVE`**: Datos actualizados en tiempo real del partido en juego.
- **`CONFIRMED`**: Datos oficiales verificados tras finalizar el encuentro o alineación oficial confirmada.
- **`PROVISIONAL`**: Alineación estimada o cuota preliminar antes del partido.
- **`PROVISIONAL_SYNTHETIC`**: Fixture de simulación para desarrollo local cuando no hay red o credenciales.
- **`STALE`**: Datos con más de 30 minutos sin refresco (muestra alerta visual al usuario).
- **`UNAVAILABLE`**: Estadística no proporcionada por la fuente (nunca se rellena con números falsos).
