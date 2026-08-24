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

    PORT: int = 8001
    DEBUG: bool = True

    # AI Provider API Keys
    OLLAMA_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    CEREBRAS_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    SAMBANOVA_API_KEY: Optional[str] = None
    NVIDIA_API_KEY: Optional[str] = None

    # Provider Enable/Disable
    OLLAMA_CLOUD_ENABLED: bool = True
    OLLAMA_LOCAL_ENABLED: bool = False
    GEMINI_ENABLED: bool = True
    GROQ_ENABLED: bool = True
    CEREBRAS_ENABLED: bool = False
    OPENROUTER_ENABLED: bool = True
    SAMBANOVA_ENABLED: bool = False
    NVIDIA_ENABLED: bool = True

    # URLs
    OLLAMA_CLOUD_URL: str = "https://api.ollama.com"
    OLLAMA_LOCAL_URL: str = "http://127.0.0.1:11434"
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"

    # Models
    OLLAMA_CLOUD_MODEL: str = "gpt-oss:120b"
    OLLAMA_LOCAL_MODEL: str = "gemma4:2b-it-qat"
    OLLAMA_QWEN_MODEL: str = "qwen3.5:2b-q4_K_M"
    OLLAMA_GEMMA_MODEL: str = "gemma4:2b-it-qat"
    GEMINI_MODEL: str = "gemini-3.6-flash"
    GEMINI_FAST_MODEL: str = "gemini-3.5-flash-lite"
    GROQ_MODEL: str = "qwen/qwen3.6-27b"
    CEREBRAS_MODEL: str = "gpt-oss-120b"
    OPENROUTER_MODEL: str = "openrouter/free"
    OPENROUTER_KIMI_K26_MODEL: str = "moonshotai/kimi-k2.6"
    OPENROUTER_KIMI_K3_MODEL: str = "moonshotai/kimi-k3"
    OPENROUTER_KIMI_CODE_MODEL: str = "moonshotai/kimi-k2.7-code"
    SAMBANOVA_MODEL: str = "llama3-70b"

    # NVIDIA Models
    NVIDIA_GPT_OSS_MODEL: str = "openai/gpt-oss-120b"
    NVIDIA_DEEPSEEK_MODEL: str = "deepseek-ai/deepseek-v4-flash-0731"
    NVIDIA_MINIMAX_MODEL: str = "minimaxai/minimax-m3"

    # Job Settings
    MAX_ACTIVE_CHAPTER_JOBS_PER_STUDENT: int = 1
    CHAPTER_PROCESSING_MODE: str = "SEQUENTIAL"
    MAX_CHAPTER_PAGES: int = 80
    REJECT_MULTI_CHAPTER_DOCUMENTS: bool = True
    MULTI_CHAPTER_MARKER_THRESHOLD: int = 2
    CHAPTER_GENERATION_TIMEOUT: int = 600  # seconds

    # Security
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000", "http://127.0.0.1:3000", "http://[::1]:3000",
        "http://localhost:3001", "http://127.0.0.1:3001", "http://[::1]:3001",
        "http://localhost:3002", "http://127.0.0.1:3002", "http://[::1]:3002",
        "http://localhost:3003", "http://127.0.0.1:3003", "http://[::1]:3003",
        "http://localhost:3004", "http://127.0.0.1:3004", "http://[::1]:3004",
        "http://localhost:3005", "http://127.0.0.1:3005", "http://[::1]:3005",
        "http://localhost:5173", "http://127.0.0.1:5173", "http://[::1]:5173",
        "http://localhost:8001", "http://127.0.0.1:8001",
        "tauri://localhost"
    ]

    # Paths
    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    MASTER_CONTENT_ROOT: str = os.path.join(PROJECT_ROOT, "backend", "GURUKUL_AI_CONTENT")
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

    # Multimedia External Catalog (Class-wise)
    MULTIMEDIA_CATALOG_FILENAME: str = "multimedia_catalog.json"
    MULTIMEDIA_EXTERNAL_API_IMPORT_PATH: str = os.path.join(MASTER_CONTENT_ROOT, "metadata", "GURUKUL_EXTERNAL_MULTIMEDIA_API_IMPORT.json")

    # General Learning (Class-wise)
    GENERAL_LEARNING_FILENAME: str = "general_learning.json"

    # Question Bank (Class-wise)
    QUESTION_BANK_FILENAME: str = "question_bank.json"

    # Metadata
    CHAPTER_TITLE_MAP_PATH: str = os.path.join(MASTER_CONTENT_ROOT, "metadata", "chapter_title_map.json")


settings = Settings()
