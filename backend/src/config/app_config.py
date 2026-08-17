import os
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

    PORT: int = 8000
    DEBUG: bool = True

    # AI Provider API Keys
    OLLAMA_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    CEREBRAS_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    SAMBANOVA_API_KEY: Optional[str] = None

    # Provider Enable/Disable
    OLLAMA_CLOUD_ENABLED: bool = True
    OLLAMA_LOCAL_ENABLED: bool = False
    GEMINI_ENABLED: bool = True
    GROQ_ENABLED: bool = True
    CEREBRAS_ENABLED: bool = False
    OPENROUTER_ENABLED: bool = True
    SAMBANOVA_ENABLED: bool = False

    # URLs
    OLLAMA_CLOUD_URL: str = "https://api.ollama.com"
    OLLAMA_LOCAL_URL: str = "http://localhost:11434"

    # Models
    OLLAMA_CLOUD_MODEL: str = "gpt-oss:120b"
    OLLAMA_LOCAL_MODEL: str = "llama3.2"
    GEMINI_MODEL: str = "gemini-3.6-flash"
    GEMINI_FAST_MODEL: str = "gemini-3.5-flash-lite"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    CEREBRAS_MODEL: str = "gpt-oss-120b"
    OPENROUTER_MODEL: str = "openrouter/free"
    SAMBANOVA_MODEL: str = "llama3-70b"

    # Job Settings
    MAX_ACTIVE_CHAPTER_JOBS_PER_STUDENT: int = 1
    CHAPTER_PROCESSING_MODE: str = "SEQUENTIAL"
    MAX_CHAPTER_PAGES: int = 80
    REJECT_MULTI_CHAPTER_DOCUMENTS: bool = True
    MULTI_CHAPTER_MARKER_THRESHOLD: int = 2
    CHAPTER_GENERATION_TIMEOUT: int = 600  # seconds

    # Security
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "tauri://localhost"
    ]

    # Paths
    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    MASTER_CONTENT_ROOT: str = os.path.join(PROJECT_ROOT, "backend", "GURUKUL_AI_FINAL_MASTER_CONTENT_CLASSES_5_6_7")
    USE_MASTER_CONTENT: bool = True

    # DIKSHA Credentials
    DIKSHA_CLASS5_USER: Optional[str] = None
    DIKSHA_CLASS5_PASS: Optional[str] = None
    DIKSHA_CLASS6_USER: Optional[str] = None
    DIKSHA_CLASS6_PASS: Optional[str] = None

    # Firebase
    FIREBASE_SERVICE_ACCOUNT_PATH: Optional[str] = None
    FIREBASE_PROJECT_ID: Optional[str] = "com-ncert-projectgurukul-e5e60"

    # Storage
    DATABASE_URL: str = "sqlite+aiosqlite:///./gurukul_backend.db"
    STORAGE_PATH: str = os.path.join(PROJECT_ROOT, "backend", "storage")

    # Test/Validation Mode
    TEST_MODE: bool = False

    # Adaptive Mastery Feature Flags
    ADAPTIVE_MASTERY_KNOWLEDGE_GRAPH: bool = True
    ADAPTIVE_MASTERY_DIAGNOSTIC: bool = True
    ADAPTIVE_MASTERY_CONCEPT_SRS: str = "ACTIVE"
    ADAPTIVE_MASTERY_ERROR_ANALYSIS: str = "ACTIVE"
    ADAPTIVE_MASTERY_INTERLEAVING: str = "ACTIVE"
    ADAPTIVE_MASTERY_REVIEW_COORDINATION: str = "ACTIVE"

    # Multimedia External Catalog
    MULTIMEDIA_EXTERNAL_CATALOG_PATH: str = os.path.join(PROJECT_ROOT, "Multimedia", "GURUKUL_EXTERNAL_MULTIMEDIA_101_CHAPTERS_V3.json")
    MULTIMEDIA_EXTERNAL_API_IMPORT_PATH: str = os.path.join(PROJECT_ROOT, "Multimedia", "GURUKUL_EXTERNAL_MULTIMEDIA_API_IMPORT.json")

    # General Learning
    GENERAL_LEARNING_DATA_PATH: str = os.path.join(PROJECT_ROOT, "General Learning", "Gurukul_General_Learning_Classes_5_6_7_Max_V1.json")


settings = Settings()
