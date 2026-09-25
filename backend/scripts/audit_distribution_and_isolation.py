import sys
import os
import time
import json
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver
from src.navigation.navigation_builder import BackendNavigationBuilder

def run_deep_audit():
    print("=== STARTING DEEP DATA-TO-UI AUDIT ===")

    files = ContentLoaderService.load_raw_subject_files("5", "English")
    notes = files.get("santoor_chapters_notes.json", {}).get("chapters", [])

    total_blocks = 0
    chapter_breakdown = []

    for c in notes:
        u = c["unitNumber"]
        ch = c["chapterNumber"]
        ch_id = f"G5-ENG-U{u:02d}-C{ch:02d}"

        # Cold fetch
        t0 = time.perf_counter()
        data = ContentLoaderService.load_chapter_source("5", "English", ch_id)
        t_load = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        adapter = AdapterResolver.resolve("NCERT", "5", "English", data)
        blocks = adapter.parse_chapter(data, ch_id)
        manifest = adapter.generate_manifest(ch_id, blocks)
        nav = BackendNavigationBuilder.build_navigation("English", manifest)
        t_proc = (time.perf_counter() - t0) * 1000

        total_blocks += len(blocks)

        types_count = {}
        for b in blocks:
            st = b.sourceType
            types_count[st] = types_count.get(st, 0) + 1

        chapter_breakdown.append({
            "unitNumber": u,
            "chapterNumber": ch,
            "chapterId": ch_id,
            "title": c.get("chapterTitle"),
            "loadTimeMs": round(t_load, 2),
            "procTimeMs": round(t_proc, 2),
            "blockCount": len(blocks),
            "types": types_count,
            "manifest": manifest.model_dump(),
            "tabs": [t["id"] for t in nav]
        })

    print(f"\nTotal Discovered Chapters: {len(chapter_breakdown)}")
    print(f"Total ContentBlocks Created: {total_blocks}")

    print("\nCHAPTER-BY-CHAPTER BREAKDOWN:")
    print(f"{'Ch ID':<16} | {'Title':<28} | {'Total Blocks':<12} | {'Load(ms)':<8} | {'Proc(ms)':<8} | {'Types Breakdown'}")
    print("-" * 110)
    for cb in chapter_breakdown:
        types_str = ", ".join([f"{k}:{v}" for k, v in cb['types'].items()])
        print(f"{cb['chapterId']:<16} | {cb['title']:<28} | {cb['blockCount']:<12} | {cb['loadTimeMs']:<8} | {cb['procTimeMs']:<8} | {types_str}")

    return chapter_breakdown, total_blocks

if __name__ == "__main__":
    run_deep_audit()
