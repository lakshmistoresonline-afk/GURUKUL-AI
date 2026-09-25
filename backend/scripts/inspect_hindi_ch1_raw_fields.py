import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

ch_source = ContentLoaderService.load_chapter_source("5", "Hindi", "G5-HIN-U01-C01")
print("--- Hindi Chapter 1 Source Fields ---")
print("grammar_extraction:", json.dumps(ch_source.get("grammar_extraction"), indent=2, ensure_ascii=False))
print("activities_and_checklist:", json.dumps(ch_source.get("activities_and_checklist"), indent=2, ensure_ascii=False))
print("character_analysis:", json.dumps(ch_source.get("character_analysis"), indent=2, ensure_ascii=False))
