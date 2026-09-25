import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def inspect_ch01():
    ch_id = "G5-ENG-U01-C01"
    data = ContentLoaderService.load_chapter_source("5", "English", ch_id)
    adapter = AdapterResolver.resolve("NCERT", "5", "English", data)
    blocks = adapter.parse_chapter(data, ch_id)

    print(f"=== CHAPTER SOURCE KEYS FOR {ch_id} ===")
    print("Title in source:", data.get("chapterTitle"))
    print("Unit Title in source:", data.get("unitTitle"))
    print("Unit Number:", data.get("unitNumber"))
    print("Chapter Number:", data.get("chapterNumber"))
    print("\nSource Keys present in data:", list(data.keys()))

    print("\n=== PARSED CONTENT BLOCKS ===")
    for b in blocks:
        print(f"Block ID: {b.id}")
        print(f"  sourceType: {b.sourceType}")
        print(f"  normalizedType: {b.normalizedType}")
        print(f"  renderer: {b.renderer}")
        print(f"  data type: {type(b.data).__name__}")
        if isinstance(b.data, dict):
            print(f"  dict keys: {list(b.data.keys())}")
        elif isinstance(b.data, list):
            print(f"  list length: {len(b.data)}")
            if len(b.data) > 0 and isinstance(b.data[0], dict):
                print(f"  first item keys: {list(b.data[0].keys())}")
        print("-" * 50)

if __name__ == "__main__":
    inspect_ch01()
