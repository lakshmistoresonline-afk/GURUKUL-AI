import os
import json
import re
from datetime import datetime

PRODUCTION_FILE = "backend/storage/video_resources_mapped.json"

def extract_video_id(url):
    if not url: return None
    match = re.search(r"(?:v=|v\/|embed\/|shorts\/|youtu\.be\/|\/v\/|\/e\/|watch\?v=|\/watch\?feature=player_embedded&v=)([^#&?]{11})", url)
    return match.group(1) if match else None

def is_search_url(url):
    if not url: return False
    return "youtube.com/results" in url or "search_query=" in url

def harden():
    if not os.path.exists(PRODUCTION_FILE):
        print(f"Error: {PRODUCTION_FILE} not found.")
        return

    with open(PRODUCTION_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    stats = {
        "total_chapters": len(data),
        "total_verified_before": 0,
        "total_verified_after": 0,
        "search_urls_removed": 0,
        "ids_extracted": 0,
        "discovery_links_count": 0
    }

    for cid, chapter in data.items():
        verified = chapter.get("verified_direct_resources", [])
        discovery = chapter.get("live_discovery_links", [])

        stats["total_verified_before"] += len(verified)
        stats["discovery_links_count"] += len(discovery)

        new_verified = []
        for res in verified:
            url = res.get("url", "")
            if is_search_url(url):
                stats["search_urls_removed"] += 1
                continue

            video_id = extract_video_id(url)
            if video_id:
                res["video_id"] = video_id
                res["url"] = f"https://www.youtube.com/watch?v={video_id}"
                stats["ids_extracted"] += 1
                new_verified.append(res)
            elif url.startswith("https://"):
                # Keep valid looking external links even if not recognized as YT?
                # No, the goal is YT fix.
                if "youtube.com" in url or "youtu.be" in url:
                    new_verified.append(res)

        chapter["verified_direct_resources"] = new_verified
        stats["total_verified_after"] += len(new_verified)

    # Backup
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = PRODUCTION_FILE.replace(".json", f".harden_backup_{ts}.json")
    with open(backup, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Save Production
    with open(PRODUCTION_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\n--- YouTube URL Hardening Report ---")
    print(f"Total Chapters:        {stats['total_chapters']}")
    print(f"Verified (Before):     {stats['total_verified_before']}")
    print(f"Verified (After):      {stats['total_verified_after']}")
    print(f"Search URLs Removed:   {stats['search_urls_removed']}")
    print(f"Video IDs Extracted:   {stats['ids_extracted']}")
    print(f"Discovery Links:       {stats['discovery_links_count']}")
    print(f"Backup saved to:       {backup}")
    print("------------------------------------\n")

if __name__ == "__main__":
    harden()
