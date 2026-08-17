import json
import os
import re
from typing import Dict, Any, List

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def validate_youtube_data():
    path = os.path.join(PROJECT_ROOT, "backend", "storage", "video_resources_mapped.json")
    if not os.path.exists(path):
        return {"status": "FAIL", "error": "File missing"}

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    errors = []
    direct_count = 0
    search_count = 0

    for cid, info in data.items():
        # Check for search URLs in verified_direct_resources
        for v in info.get("verified_direct_resources", []):
            url = v.get("url", "")
            if "youtube.com/results" in url or "search_query=" in url:
                errors.append(f"{cid}: Search URL found in verified_direct_resources: {url}")
            else:
                direct_count += 1

        # Check discovery links
        for d in info.get("live_discovery_links", []):
            search_count += 1

    return {
        "status": "PASS" if not errors else "FAIL",
        "direct_videos": direct_count,
        "discovery_links": search_count,
        "errors": errors
    }

def validate_general_learning():
    path = os.path.join(PROJECT_ROOT, "General Learning", "Gurukul_General_Learning_Classes_5_6_7_Max_V1.json")
    if not os.path.exists(path):
        return {"status": "FAIL", "error": "File missing"}

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    content = data.get("content", [])
    errors = []
    for idx, item in enumerate(content):
        if "srsEligible" not in item:
            # Not an error but worth noting
            pass
        if not item.get("classId"):
            errors.append(f"Item {idx}: Missing classId")

    return {
        "status": "PASS" if not errors else "FAIL",
        "total_records": len(content),
        "errors": errors
    }

def run_all():
    report = {
        "youtube": validate_youtube_data(),
        "general_learning": validate_general_learning(),
    }

    with open(os.path.join(PROJECT_ROOT, "validation_report.json"), 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    run_all()
