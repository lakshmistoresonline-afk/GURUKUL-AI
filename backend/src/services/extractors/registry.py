import logging
from typing import Dict, Any, List, Optional
from .base_extractor import BaseExtractor
from .pdf_extractor import PDFExtractor
from .video_extractor import VideoExtractor
from .archive_extractor import ArchiveExtractor

logger = logging.getLogger(__name__)

class ExtractionRegistry:
    def __init__(self):
        self.extractors: Dict[str, BaseExtractor] = {
            "PDF": PDFExtractor(),
            "VIDEO": VideoExtractor(),
            "ZIP": ArchiveExtractor(),
            "INTERACTIVE": ArchiveExtractor(),
            "EPUB": ArchiveExtractor(), # Simple fallback
        }
        self.default_extractor = ArchiveExtractor() # Generic fallback

    def get_extractor(self, content_type: str) -> BaseExtractor:
        return self.extractors.get(content_type.upper(), self.default_extractor)

    async def run_extraction(self, file_path: str, content_type: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        extractor = self.get_extractor(content_type)
        logger.info(f"Using {extractor.__class__.__name__} for type {content_type}")
        return await extractor.extract(file_path, metadata)

extraction_registry = ExtractionRegistry()
