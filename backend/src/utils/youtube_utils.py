import re
from typing import Dict, Any, Optional

def extract_video_id(url: str) -> Optional[str]:
    """
    Extracts the 11-character YouTube video ID from various URL formats.
    """
    if not url:
        return None

    # Regex for various YT formats
    pattern = r"(?:v=|v\/|embed\/|shorts\/|youtu\.be\/|\/v\/|\/e\/|watch\?v=|\/watch\?feature=player_embedded&v=)([^#&?]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def is_search_url(url: str) -> bool:
    """
    Detects if a URL is a YouTube search/results URL.
    """
    if not url:
        return False
    return "youtube.com/results" in url or "search_query=" in url

def normalize_youtube_resource(url: str) -> Dict[str, Any]:
    """
    Analyzes a URL and returns structured data about the YouTube resource.
    """
    if not url:
        return {"type": "INVALID", "is_playable": False}

    if is_search_url(url):
        return {
            "type": "DISCOVERY_SEARCH",
            "url": url,
            "is_playable": False
        }

    video_id = extract_video_id(url)
    if video_id:
        return {
            "type": "DIRECT_VIDEO",
            "video_id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "is_playable": True
        }

    # Fallback for unrecognized but potentially valid YT links
    if "youtube.com" in url or "youtu.be" in url:
         return {"type": "UNVERIFIED_YOUTUBE", "url": url, "is_playable": False}

    return {"type": "NON_YOUTUBE", "url": url, "is_playable": False}
