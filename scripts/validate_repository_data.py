import os
import json
import re
from datetime import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_STORAGE = os.path.join(PROJECT_ROOT, "backend", "storage")
YOUTUBE_MAPPING = os.path.join(BACKEND_STORAGE, "video_resources_mapped.json")
GENERAL_LEARNING = os.path.join(PROJECT_ROOT, "General Learning", "Gurukul_General_Learning_Classes_5_6_7_Max_V1.json")

def validate_youtube():
    if not os.path.exists(YOUTUBE_MAPPING):
        return {"error": "YouTube mapping file not found"}

    with open(YOUTUBE_MAPPING, 'r', encoding='utf-8') as f:
        data = json.load(f)

    report = {
        "total_chapters": len(data),
        "verified_direct": 0,
        "discovery_links": 0,
        "search_urls_in_verified": 0,
        "malformed_urls": 0
    }

    for cid, chapter in data.items():
        verified = chapter.get("verified_direct_resources", [])
        discovery = chapter.get("live_discovery_links", [])

        report["verified_direct"] += len(verified)
        report["discovery_links"] += len(discovery)

        for res in verified:
            url = res.get("url", "")
            if "youtube.com/results" in url or "search_query=" in url:
                report["search_urls_in_verified"] += 1
            if not (url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://youtu.be/")):
                if "youtube.com" in url or "youtu.be" in url:
                    report["malformed_urls"] += 1

    return report

def validate_general_learning():
    if not os.path.exists(GENERAL_LEARNING):
        return {"error": "General learning data not found"}

    with open(GENERAL_LEARNING, 'r', encoding='utf-8') as f:
        data = json.load(f)

    content = data.get("content", [])
    report = {
        "total_items": len(content),
        "by_class": {},
        "srs_eligible": 0,
        "missing_fields": 0
    }

    for item in content:
        c_id = item.get("classId")
        report["by_class"][c_id] = report["by_class"].get(c_id, 0) + 1
        if item.get("srsEligible"):
            report["srs_eligible"] += 1

        if item.get("type") == "vocabulary":
            if not item.get("word") or not item.get("meaning"):
                report["missing_fields"] += 1
        else:
            if not item.get("question") or not item.get("answer"):
                report["missing_fields"] += 1

    return report

def main():
    print(f"Starting Repository Data Validation at {datetime.now()}")

    yt_report = validate_youtube()
    gl_report = validate_general_learning()

    final_report = {
        "timestamp": datetime.now().isoformat(),
        "youtube": yt_report,
        "general_learning": gl_report,
        "status": "PASS" if yt_report.get("search_urls_in_verified", 0) == 0 else "WARNING"
    }

    output_path = os.path.join(PROJECT_ROOT, "validation_report.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2)

    print(f"Validation Report saved to {output_path}")
    print(json.dumps(final_report, indent=2))

if __name__ == "__main__":
    main()
