import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def audit_all_other_subjects():
    root = r"D:\GURUKUL\Contents\Class 5"

    print("==========================================================================")
    print("MASTER DATASETS FIELD-BY-FIELD AUDIT: HINDI, MATHS, AND SCIENCE")
    print("==========================================================================\n")

    # 1. HINDI MASTER AUDIT
    hin_path = os.path.join(root, "Hindi", "Hindi Master.json")
    hin_raw = json.load(open(hin_path, encoding="utf-8"))
    hin_chs = hin_raw.get("chapters_master_data", [])
    print(f"1. HINDI MASTER DATASET ({len(hin_chs)} Chapters):")
    print(f"   Book Title: {hin_raw.get('book_title')}")
    print(f"   Exam Structure: {hin_raw.get('exam_structure')}")

    for i, ch in enumerate(hin_chs, 1):
        info = ch.get("chapter_info", {})
        c_num = ch.get("chapter_number")
        c_title = info.get("title_hindi") or info.get("title") or ch.get("chapter_title")

        ch_id = f"G5-HIN-U{((c_num-1)//3)+1:02d}-C{c_num:02d}"
        ch_source = ContentLoaderService.load_chapter_source("5", "Hindi", ch_id)
        adapter = AdapterResolver.resolve("NCERT", "5", "Hindi", ch_source)
        blocks = adapter.parse_chapter(ch_source, ch_id)

        print(f"   Ch {c_num}: {c_title} -> {len(blocks)} ContentBlocks: {[b.sourceType for b in blocks]}")
    print("-" * 74)

    # 2. SCIENCE MASTER AUDIT
    sci_path = os.path.join(root, "Science", "Science Master.json")
    sci_raw = json.load(open(sci_path, encoding="utf-8"))
    sci_chs = sci_raw.get("chapters", [])
    print(f"\n2. SCIENCE MASTER DATASET ({len(sci_chs)} Chapters):")
    print(f"   Framework: {sci_raw.get('curriculumFramework')}")
    print(f"   Title: {sci_raw.get('title')}")

    for i, ch in enumerate(sci_chs, 1):
        c_num = ch.get("chapterNumber")
        c_title = ch.get("chapterTitle")

        ch_id = f"G5-SCI-U{((c_num-1)//3)+1:02d}-C{c_num:02d}"
        ch_source = ContentLoaderService.load_chapter_source("5", "Science", ch_id)
        adapter = AdapterResolver.resolve("NCERT", "5", "Science", ch_source)
        blocks = adapter.parse_chapter(ch_source, ch_id)

        print(f"   Ch {c_num}: {c_title} -> {len(blocks)} ContentBlocks: {[b.sourceType for b in blocks]}")
    print("-" * 74)

    # 3. MATHS MASTER AUDIT
    math_path = os.path.join(root, "Maths", "Maths Master.json")
    math_raw = json.load(open(math_path, encoding="utf-8"))
    math_notes = math_raw.get("chapter_notes", [])
    print(f"\n3. MATHS MASTER DATASET ({len(math_notes)} Chapters):")
    print(f"   App Title: {math_raw.get('app_title')}")
    print(f"   Curriculum: {math_raw.get('curriculum')}")

    for i, ch in enumerate(math_notes, 1):
        c_num = ch.get("chapter_number")
        c_title = ch.get("chapter_title")

        ch_id = f"G5-MAT-U{((c_num-1)//3)+1:02d}-C{c_num:02d}"
        ch_source = ContentLoaderService.load_chapter_source("5", "Maths", ch_id)
        adapter = AdapterResolver.resolve("NCERT", "5", "Maths", ch_source)
        blocks = adapter.parse_chapter(ch_source, ch_id)

        print(f"   Ch {c_num}: {c_title} -> {len(blocks)} ContentBlocks: {[b.sourceType for b in blocks]}")
    print("-" * 74)

if __name__ == "__main__":
    audit_all_other_subjects()
