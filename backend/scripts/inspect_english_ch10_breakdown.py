import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

ch_source = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U05-C10")
print("--- English Ch 10 Detailed Breakdown ---")
print(json.dumps(ch_source.get("detailedBreakdown"), indent=2, ensure_ascii=False))
