# PARLAYIQ — Guía de Despliegue y Puesta en Producción

## 1. Requisitos Previos

- **Python**: 3.11 o superior (recomendado 3.12 con `uv`).
- **Node.js**: v18 o superior (probado en v24 con `npm`).
- **Base de Datos**: SQLite (modo local / sin dependencias externas) o PostgreSQL 15/16 para producción.
- **Docker y Docker Compose**: Para despliegue contenerizado.

---

## 2. Puesta en Marcha Local en Desarrollo

### A. Backend (FastAPI + Motor Cuantitativo)
```bash
cd backend

# Crear y activar entorno virtual con uv
uv venv --python 3.12
.\.venv\Scripts\activate   # En Windows
# source .venv/bin/activate # En Linux/macOS

# Instalar dependencias
uv pip install -r requirements.txt greenlet

# Ejecutar la suite completa de pruebas unitarias y de integración
uv run python run_tests.py

# Iniciar servidor FastAPI
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- API activa en: `http://localhost:8000`
- Documentación Swagger interactiva: `http://localhost:8000/docs`

### B. Frontend (Next.js 14 + Tailwind CSS)
```bash
cd frontend

# Instalar dependencias
npm install

# Compilar para producción
npm run build

# O iniciar en modo desarrollo
npm run dev
```
- Frontend accesible en: `http://localhost:3000`

---

## 3. Despliegue con Docker Compose en Servidor / VPS

```bash
cd infrastructure
docker-compose up --build -d
```
Servicios desplegados:
- `parlayiq_backend`: Puerto 8000
- `parlayiq_frontend`: Puerto 3000
- `parlayiq_postgres`: PostgreSQL 16 con healthcheck automático
- `parlayiq_redis`: Redis 7 para caching de cuotas y live ticks

---

## 4. Configuración de Proveedores Deportivos

Cuando dispongas de credenciales de proveedores deportivos pagos o gratuitos (API-Football, The Odds API, football-data.org):
1. Edita el archivo `.env` en la raíz del proyecto.
2. Añade las claves correspondientes:
   ```env
   API_FOOTBALL_KEY=tu_clave_aqui
   FOOTBALL_DATA_ORG_KEY=tu_clave_aqui
   THE_ODDS_API_KEY=tu_clave_aqui
   ```
3. Reinicia el backend: el adaptador detectará automáticamente las credenciales y cambiará el estado de `CONFIGURATION_REQUIRED` a `CONNECTED`.
