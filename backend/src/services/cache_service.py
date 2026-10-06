import hashlib
from typing import Dict, Any, Optional
from src.curriculum.core.curriculum_identity import CurriculumIdentity

class CurriculumCacheService:
    """
    Production-grade curriculum cache service enforcing complete identity isolation
    including grade, subject, book/part, unit, chapter, content_type, and schema version.
    """
    _MEMORY_CACHE: Dict[str, Any] = {}

    @classmethod
    def generate_cache_key(cls, identity: CurriculumIdentity, schema_version: str = "3.0.0") -> str:
        base_key = identity.to_cache_key()
        full_key = f"{base_key}:schema:{schema_version}"
        # Return hashed key or structured canonical key
        return full_key

    @classmethod
    def get(cls, identity: CurriculumIdentity, schema_version: str = "3.0.0") -> Optional[Any]:
        key = cls.generate_cache_key(identity, schema_version)
        return cls._MEMORY_CACHE.get(key)

    @classmethod
    def set(cls, identity: CurriculumIdentity, data: Any, schema_version: str = "3.0.0"):
        key = cls.generate_cache_key(identity, schema_version)
        cls._MEMORY_CACHE[key] = data

    @classmethod
    def clear(cls):
        cls._MEMORY_CACHE.clear()
