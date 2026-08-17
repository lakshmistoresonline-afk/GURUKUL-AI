import pyttsx3
import os
import logging
import uuid
from typing import Optional

logger = logging.getLogger(__name__)

class TTSService:
    """
    Local Text-to-Speech service using pyttsx3.
    """

    def __init__(self):
        self.engine = pyttsx3.init()
        # Set property before adding anything to queue
        self.engine.setProperty('rate', 150)    # Speed percent (can go over 100)
        self.engine.setProperty('volume', 0.9)  # Volume 0-1

        # Try to find a good English voice
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "english" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break

    def synthesize(self, text: str, output_path: str) -> bool:
        """Synthesize text to an audio file (wav/mp3)."""
        try:
            # pyttsx3 is synchronous in its default save_to_file loop
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            return os.path.exists(output_path)
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            return False
