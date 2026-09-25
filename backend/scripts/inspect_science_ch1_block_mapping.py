import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

ch_source = ContentLoaderService.load_chapter_source("5", "Science", "G5-SCI-U01-C01")
adapter = AdapterResolver.resolve("NCERT", "5", "Science", ch_source)
blocks = adapter.parse_chapter(ch_source, "G5-SCI-U01-C01")

print(f"Total blocks for Science Ch 1: {len(blocks)}")
for b in blocks:
    print(f"\nBlock ID: {b.id}")
    print(f"  sourceType: {b.sourceType}")
    print(f"  normalizedType: {b.normalizedType}")
    print(f"  renderer: {b.renderer}")
    print(f"  title: {b.title}")
    if isinstance(b.data, dict):
        print(f"  data keys: {list(b.data.keys())}")
        if "details" in b.data:
            print(f"  details len: {len(b.data['details']) if isinstance(b.data['details'], list) else type(b.data['details'])}")
            if isinstance(b.data['details'], list) and b.data['details']:
                print(f"    Sample detail 0: {b.data['details'][0]}")
    elif isinstance(b.data, list):
        print(f"  data list len: {len(b.data)}")
        if b.data:
            print(f"    Sample item 0: {b.data[0]}")
