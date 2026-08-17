import os
import logging
from typing import Dict, Any, List
from .base_extractor import BaseExtractor

logger = logging.getLogger(__name__)

class VideoExtractor(BaseExtractor):
    """
    Transcribes video content using OpenAI Whisper.
    Strict Invariant: Fails if real transcription cannot be completed.
    """
    def __init__(self):
        self.model = None

    def _load_model(self):
        if self.model is None:
            import whisper
            self.model = whisper.load_model("base")

    async def extract(self, file_path: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        logger.info(f"RAG: Attempting real transcription for {file_path}")
        try:
            self._load_model()

            # Check for ffmpeg dependency
            import shutil
            if not shutil.which("ffmpeg"):
                raise RuntimeError("ffmpeg not found in system path. Real video transcription is blocked.")

            # Real Whisper call
            result = self.model.transcribe(file_path)
            segments = result.get('segments', [])

            if not segments:
                raise ValueError("Whisper produced no transcript segments for this binary.")

            chunks = []
            current_text = ""
            start_t = 0.0

            for seg in segments:
                current_text += seg['text'] + " "
                if len(current_text) > 800:
                    chunks.append({
                        "text": current_text.strip(),
                        "metadata": {
                            **metadata,
                            "start_time": start_t,
                            "end_time": seg['end']
                        }
                    })
                    current_text = ""
                    start_t = seg['end']

            if current_text:
                chunks.append({
                    "text": current_text.strip(),
                    "metadata": {
                        **metadata,
                        "start_time": start_t,
                        "end_time": segments[-1]['end'] if segments else 0.0
                    }
                })

            return chunks

        except Exception as e:
            logger.error(f"Video Extraction Error for {metadata.get('title')}: {e}")
            raise # Let resource_service catch and mark as RAG_FAILED
