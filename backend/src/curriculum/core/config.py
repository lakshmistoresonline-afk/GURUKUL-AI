import os
from pathlib import Path

class GurukulConfig:
    """
    Centralized configuration for Gurukul AI curriculum paths.
    Consumes environment variables GURUKUL_CONTENT_ROOT and GURUKUL_PROCESSED_ROOT,
    with safe repository-relative defaults from repository root.
    """
    REPO_ROOT = Path(__file__).resolve().parents[4]

    @classmethod
    def get_content_root(cls) -> Path:
        env_val = os.getenv("GURUKUL_CONTENT_ROOT")
        if env_val:
            return Path(env_val).resolve()
        return (cls.REPO_ROOT / "Contents").resolve()

    @classmethod
    def get_processed_root(cls) -> Path:
        env_val = os.getenv("GURUKUL_PROCESSED_ROOT")
        if env_val:
            return Path(env_val).resolve()
        return (cls.REPO_ROOT / "ProcessedContent").resolve()
