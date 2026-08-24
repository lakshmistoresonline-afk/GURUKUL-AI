import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.utils.path_resolver import PathResolver
from src.config.app_config import settings

def test():
    print(f"MASTER_CONTENT_ROOT: {settings.MASTER_CONTENT_ROOT}")

    for cid in ["5", "6", "7"]:
        print(f"\n--- Testing Class {cid} ---")
        hierarchy = PathResolver.get_class_hierarchy(cid)
        print(f"Subjects found: {list(hierarchy.keys())}")

        for sub, chapters in hierarchy.items():
            print(f"  {sub}: {len(chapters)} chapters")
            if chapters:
                print(f"    Example: {chapters[0]}")

        # Test path resolution for a known chapter
        if cid == "6":
            path = PathResolver.get_chapter_path("6", "fepr101", subject="English")
            print(f"Path for fepr101 (English): {path}")

if __name__ == "__main__":
    test()
