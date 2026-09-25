from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from ..core.models import ContentBlock, ContentManifest, ContentTypeManifestItem

class BaseContentAdapter(ABC):
    """Abstract base class for content adapters."""

    ADAPTER_VERSION = "2.0.0"

    @abstractmethod
    def parse_chapter(
        self,
        source_data: Dict[str, Any],
        chapter_id: str,
        source_dataset: str = "NCERT"
    ) -> List[ContentBlock]:
        """Converts source JSON data into a list of normalized ContentBlock items."""
        pass

    def generate_manifest(self, chapter_id: str, blocks: List[ContentBlock]) -> ContentManifest:
        """Generates a ContentManifest summary from normalized ContentBlock items."""
        manifest_items: List[ContentTypeManifestItem] = []

        for block in blocks:
            manifest_items.append(
                ContentTypeManifestItem(
                    type=block.normalizedType,
                    sourceType=block.sourceType,
                    learningStage=block.learningStage,
                    presentationSection=block.presentationSection,
                    count=1,
                    renderer=block.renderer
                )
            )

        return ContentManifest(
            chapterId=chapter_id,
            contentTypes=manifest_items,
            adapterVersion=self.ADAPTER_VERSION
        )
