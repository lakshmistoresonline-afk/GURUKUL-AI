import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

ch_source = ContentLoaderService.load_chapter_source("5", "Science", "G5-SCI-U01-C01")
print("Science Ch 1 raw source keys:", list(ch_source.keys()))
print("Science Ch 1 'overview' type:", type(ch_source.get("overview")), ch_source.get("overview"))
print("Science Ch 1 'mindmap':", ch_source.get("mindmap"))

adapter = AdapterResolver.resolve("NCERT", "5", "Science", ch_source)
blocks = adapter.parse_chapter(ch_source, "G5-SCI-U01-C01")
print(f"\nParsed {len(blocks)} blocks:")
for b in blocks:
    print(f"  {b.id:<35} | {b.sourceType:<20} | {b.normalizedType:<20} | {b.renderer:<20}")
