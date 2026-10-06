from typing import Dict, Any, Optional
from src.curriculum.core.curriculum_identity import CurriculumIdentity

class CurriculumCacheService:
    """
    Production-grade curriculum cache service enforcing complete identity isolation
    including grade, subject, book, part, unit, chapter_id, content_type, and schema version.
    Zero cache collision guarantee across Maths I vs Maths II, Class 5 vs 6, English vs Hindi, etc.
    """
    _MEMORY_CACHE: Dict[str, Any] = {}

    @classmethod
    def generate_cache_key(cls, identity: CurriculumIdentity, schema_version: str = "3.0.0") -> str:
        # Full identity-driven cache key
        return f"grade:{identity.grade}:subj:{identity.subject.lower()}:book:{identity.book.lower()}:part:{identity.part.lower()}:unit:{identity.unit.upper()}:ch:{identity.chapter_id.lower()}:ct:{identity.content_type.lower()}:schema:{schema_version}"

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
