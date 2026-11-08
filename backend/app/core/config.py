import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "PARLAYIQ"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "parlayiq-super-secret-key-change-in-production-2026-quant-engine"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database: Supports SQLite Async (default zero-friction) and PostgreSQL Async
    DATABASE_URL: str = "sqlite+aiosqlite:///./parlayiq.db"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    
    # Sports API Provider Keys (Optional: works with open datasets & fallback if absent)
    API_FOOTBALL_KEY: str = ""
    FOOTBALL_DATA_ORG_KEY: str = ""
    THE_ODDS_API_KEY: str = ""
    
    # Monte Carlo Settings
    DEFAULT_MONTE_CARLO_SIMULATIONS: int = 10000
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
