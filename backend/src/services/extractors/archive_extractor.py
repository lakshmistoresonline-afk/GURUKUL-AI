import os
import zipfile
import json
import logging
import tempfile
import shutil
from typing import Dict, Any, List
from .base_extractor import BaseExtractor

logger = logging.getLogger(__name__)

class ArchiveExtractor(BaseExtractor):
    async def extract(self, file_path: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Safely extracts educational content from Sunbird ECML / ZIP packages.
        """
        temp_dir = tempfile.mkdtemp()
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Security: Check for path traversal
                for member in zip_ref.infolist():
                    if os.path.isabs(member.filename) or ".." in member.filename:
                        raise ValueError(f"Malicious path detected in zip: {member.filename}")

                zip_ref.extractall(temp_dir)

            extracted_text = []

            # 1. Look for index.json or manifest.json (ECML)
            manifest_path = os.path.join(temp_dir, "manifest.json")
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    try:
                        m_data = json.load(f)
                        extracted_text.append(f"Manifest Data: {json.dumps(m_data, indent=2)}")
                    except: pass

            # 2. Extract text from HTML, MD, JSON files
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith(('.html', '.htm', '.txt', '.md', '.json')):
                        p = os.path.join(root, file)
                        try:
                            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if len(content) > 50: # Skip small files
                                    extracted_text.append(f"--- File: {file} ---\n{content}")
                        except: pass

            full_text = "\n\n".join(extracted_text)
            if not full_text:
                # Fallback to metadata
                full_text = f"Educational Package: {metadata.get('title')}. {metadata.get('description', '')}"

            chunks = self.chunk_text(full_text)
            return [
                {
                    "text": chunk,
                    "metadata": {
                        **metadata,
                        "chunk_index": i
                    }
                }
                for i, chunk in enumerate(chunks)
            ]

        finally:
            shutil.rmtree(temp_dir)
