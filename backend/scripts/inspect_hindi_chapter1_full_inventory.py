import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def inspect_ch1():
    print("==========================================================================")
    print("HINDI CHAPTER 1 FULL SOURCE INVENTORY & TRACE")
    print("==========================================================================\n")

    files = ContentLoaderService.load_raw_subject_files("5", "Hindi")
    notes_chapters = files.get("Notes.json", {}).get("chapters", [])
    master_chapters = files.get("Hindi Master.json", {}).get("chapters_master_data", [])

    ch1_notes = notes_chapters[0] if notes_chapters else {}
    ch1_master = master_chapters[0] if master_chapters else {}

    print("--- Notes.json Chapter 1 ---")
    for k, v in ch1_notes.items():
        if isinstance(v, list):
            print(f"  {k}: list with {len(v)} items")
        elif isinstance(v, dict):
            print(f"  {k}: dict with keys {list(v.keys())}")
        else:
            print(f"  {k}: {v}")

    print("\n--- Hindi Master.json Chapter 1 ---")
    for k, v in ch1_master.items():
        if isinstance(v, list):
            print(f"  {k}: list with {len(v)} items")
        elif isinstance(v, dict):
            print(f"  {k}: dict with keys {list(v.keys())}")
        else:
            print(f"  {k}: {v}")

    ch_source = ContentLoaderService.load_chapter_source("5", "Hindi", "G5-HIN-U01-C01")
    adapter = AdapterResolver.resolve("NCERT", "5", "Hindi", ch_source)
    blocks = adapter.parse_chapter(ch_source, "G5-HIN-U01-C01")

    print(f"\nTotal ContentBlocks parsed for Hindi Ch 1: {len(blocks)}")
    for b in blocks:
        print(f"  Block ID: {b.id:<35} | sourceType: {b.sourceType:<25} | renderer: {b.renderer:<20}")

if __name__ == "__main__":
    inspect_ch1()
