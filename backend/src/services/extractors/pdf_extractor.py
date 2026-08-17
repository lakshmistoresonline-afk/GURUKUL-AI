from typing import Dict, Any, List
from .base_extractor import BaseExtractor
from ...utils.pdf_utils import extract_pdf_text

class PDFExtractor(BaseExtractor):
    async def extract(self, file_path: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        text = extract_pdf_text(file_path)
        if not text:
            return []

        chunks = self.chunk_text(text)
        return [
            {
                "text": chunk,
                "metadata": {
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            }
            for i, chunk in enumerate(chunks)
        ]
