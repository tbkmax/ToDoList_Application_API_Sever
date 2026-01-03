from typing import Optional
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: str = "5432"

    class Config:
        env_file = ".env"


settings = Settings()

# If `DATABASE_URL` is not provided, build it from POSTGRES_* environment vars
if not settings.database_url:
    user = settings.POSTGRES_USER or os.getenv("POSTGRES_USER")
    pw = settings.POSTGRES_PASSWORD or os.getenv("POSTGRES_PASSWORD")
    db = settings.POSTGRES_DB or os.getenv("POSTGRES_DB")
    host = settings.POSTGRES_HOST or os.getenv("POSTGRES_HOST", "db")
    port = settings.POSTGRES_PORT or os.getenv("POSTGRES_PORT", "5432")
    if user and pw and db:
        settings.database_url = f"postgresql+asyncpg://{user}:{pw}@{host}:{port}/{db}"
