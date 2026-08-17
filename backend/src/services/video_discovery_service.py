import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class VideoDiscoveryService:
    """
    Video Discovery is currently disabled as per user request to remove YouTube links.
    """

    def __init__(self, session_factory):
        self.AsyncSession = session_factory

    async def discover_videos_for_chapter(self, class_level: str, subject: str, chapter_id: str, topic: str) -> List[Dict[str, Any]]:
        """
        Returns an empty list as video discovery is disabled.
        """
        return []

    async def _get_cached_videos(self, class_level: str, subject: str, chapter_id: str) -> List[Dict[str, Any]]:
        return []

    async def _persist_videos(self, videos: Any):
        pass
