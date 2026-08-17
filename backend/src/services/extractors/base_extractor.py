from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseExtractor(ABC):
    """
    Abstract base class for content extractors.
    """

    @abstractmethod
    async def extract(self, file_path: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract content from a file and return a list of chunks.
        Each chunk should be a dict: { "text": str, "metadata": Dict }
        """
        pass

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """Simple text chunking utility."""
        if not text: return []
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunks.append(text[i:i + chunk_size])
        return chunks
