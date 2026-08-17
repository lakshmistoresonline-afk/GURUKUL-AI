import os
import json
import logging
from fastapi import APIRouter, HTTPException, Depends
from ..config.app_config import settings
from ..utils.security import get_authorized_class, validate_chapter_access
from ..utils.auth import get_current_user, AuthUser
from ..utils.youtube_utils import normalize_youtube_resource

router = APIRouter()
logger = logging.getLogger(__name__)

MAPPED_VIDEOS_PATH = os.path.join(settings.STORAGE_PATH, "video_resources_mapped.json")

@router.get("/chapter/{chapter_id}")
async def get_chapter_videos(
    chapter_id: str,
    user: AuthUser = Depends(get_current_user)
):
    """Retrieve video resources for a specific chapter with strict class isolation and URL normalization."""
    authorized_class = user.class_name
    validate_chapter_access(chapter_id, authorized_class)

    if not os.path.exists(MAPPED_VIDEOS_PATH):
        raise HTTPException(status_code=404, detail="Video resource index not found.")

    try:
        with open(MAPPED_VIDEOS_PATH, "r", encoding="utf-8") as f:
            all_videos = json.load(f)

        chapter_data = all_videos.get(chapter_id)
        if not chapter_data:
             # Case-insensitive fallback
             for cid, data in all_videos.items():
                 if cid.lower() == chapter_id.lower():
                     chapter_data = data
                     break

             if not chapter_data:
                 return {"verified_direct_resources": [], "live_discovery_links": []}

        # Validate and Normalize verified_direct_resources
        # A student should only see direct, playable videos in this section.
        verified = []
        for v in chapter_data.get("verified_direct_resources", []):
            url = v.get("url", "")
            norm = normalize_youtube_resource(url)

            if norm["type"] == "DIRECT_VIDEO":
                v["video_id"] = norm["video_id"]
                v["url"] = norm["url"]
                v["is_direct"] = True
                verified.append(v)
            else:
                logger.warning(f"Excluding non-direct video from verified list for chapter {chapter_id}: {url}")

        # Process Discovery Links
        # Students should NOT see search result links as primary multimedia nodes.
        discovery = []
        for d in chapter_data.get("live_discovery_links", []):
            url = d.get("url", "")
            norm = normalize_youtube_resource(url)

            # If a discovery link is actually a direct video, move it or mark it
            if norm["type"] == "DIRECT_VIDEO":
                d["video_id"] = norm["video_id"]
                d["url"] = norm["url"]
                d["is_direct"] = True
                discovery.append(d)
            elif norm["type"] == "DISCOVERY_SEARCH":
                # Keep as discovery link but ensured classified correctly
                d["is_direct"] = False
                discovery.append(d)

        return {
            "chapter_id": chapter_id,
            "verified_direct_resources": verified,
            "live_discovery_links": discovery,
            "direct_count": len(verified),
            "discovery_count": len([d for d in discovery if not d.get("is_direct", False)])
        }
    except Exception as e:
        logger.error(f"Error reading video data: {e}")
        raise HTTPException(status_code=500, detail="Internal error retrieving video resources.")

@router.get("/recommendations")
async def get_video_recommendations(user: AuthUser = Depends(get_current_user)):
    """Video recommendations are currently scoped to the student's class."""
    # Placeholder for future implementation
    return []
