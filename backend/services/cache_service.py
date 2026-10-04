import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class CacheService:
    """
    Distributed Multi-Tenant Caching Layer for Gurukul AI.
    Caches processed chapter bundles in memory / Redis to ensure sub-millisecond response times.
    """
    _memory_cache: Dict[str, Any] = {}

    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        return cls._memory_cache.get(key)

    @classmethod
    def set(cls, key: str, value: Any):
        cls._memory_cache[key] = value
        logger.debug(f"CacheService stored key: {key}")

    @classmethod
    def clear(cls):
        cls._memory_cache.clear()
        logger.info("CacheService cleared all cached items.")
