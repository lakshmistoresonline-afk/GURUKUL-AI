import os
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class FFmpegService:
    """
    Handles video processing, clip concatenation, and audio merging.
    """

    def __init__(self):
        self.ffmpeg_path = "ffmpeg" # Assumes in PATH

    def check_availability(self) -> bool:
        try:
            subprocess.run([self.ffmpeg_path, "-version"], capture_output=True, check=True)
            return True
        except:
            return False

    def generate_thumbnail(self, video_path: str, thumbnail_path: str) -> bool:
        """Extract a frame from the video as a thumbnail."""
        if not os.path.exists(video_path):
            return False

        try:
            command = [
                self.ffmpeg_path, "-i", video_path,
                "-ss", "00:00:01", "-vframes", "1",
                "-y", thumbnail_path
            ]
            subprocess.run(command, capture_output=True, check=True)
            return True
        except Exception as e:
            logger.error(f"FFmpeg thumbnail generation failed: {e}")
            return False

    def merge_audio_video(self, video_path: str, audio_path: str, output_path: str) -> bool:
        """Merge an audio track with a video track."""
        try:
            command = [
                self.ffmpeg_path, "-i", video_path, "-i", audio_path,
                "-c:v", "copy", "-c:a", "aac", "-strict", "experimental",
                "-y", output_path
            ]
            subprocess.run(command, capture_output=True, check=True)
            return True
        except Exception as e:
            logger.error(f"FFmpeg audio/video merge failed: {e}")
            return False
