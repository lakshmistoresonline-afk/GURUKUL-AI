import os
from datetime import datetime
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            ".env",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PORT: int = 8001
    DEBUG: bool = True

    # Canonical Content Root
    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    CONTENT_ROOT: str = os.getenv("CONTENT_ROOT", os.path.join(PROJECT_ROOT, "Contents"))

    # AI Provider API Keys
    OLLAMA_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    CEREBRAS_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    SAMBANOVA_API_KEY: Optional[str] = None
    NVIDIA_API_KEY: Optional[str] = None

    # Security
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000", "http://127.0.0.1:3000", "http://[::1]:3000",
        "http://localhost:3001", "http://127.0.0.1:3001", "http://[::1]:3001",
        "http://localhost:8001", "http://127.0.0.1:8001",
        "tauri://localhost"
    ]

    # Storage
    DATABASE_URL: str = "sqlite+aiosqlite:///./gurukul_backend.db"
    STORAGE_PATH: str = os.path.join(PROJECT_ROOT, "backend", "storage")


settings = Settings()
