import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def audit_dashboard_counts():
    print("==========================================================================")
    print("DASHBOARD & SUBJECT MASTER ITEM COUNTS AUDIT ACROSS ALL SUBJECTS")
    print("==========================================================================\n")

    subjects = ["English", "Hindi", "Maths", "Science"]

    for sub in subjects:
        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        units = meta.get("units", [])

        total_chapters = sum(len(u.get("chapters", [])) for u in units)
        print(f"SUBJECT: Class 5 {sub}")
        print(f"  Curriculum Framework: {meta.get('curriculumFramework')}")
        print(f"  Curricular Goals Count: {len(meta.get('curricularGoals', []))}")
        print(f"  Total Units: {len(units)} | Total Chapters: {total_chapters}")

        chapter_stats = []
        for u in units:
            u_num = u.get("unitNumber", 1)
            for ch in u.get("chapters", []):
                ch_num = ch.get("chapterNumber", 1)
                ch_id = ch.get("id") or f"G5-{sub[:3].upper()}-U{u_num:02d}-C{ch_num:02d}"

                # Load chapter source & parse blocks
                ch_source = ContentLoaderService.load_chapter_source("5", sub, ch_id)
                if ch_source:
                    adapter = AdapterResolver.resolve("NCERT", "5", sub, ch_source)
                    blocks = adapter.parse_chapter(ch_source, ch_id)
                    manifest = adapter.generate_manifest(ch_id, blocks)

                    types_list = [item.type for item in manifest.contentTypes]

                    chapter_stats.append({
                        "ch_id": ch_id,
                        "title": ch.get("title") or ch_source.get("chapterTitle"),
                        "block_count": len(blocks),
                        "content_types": types_list
                    })

        print(f"  Processed Chapters Count: {len(chapter_stats)}")
        for stat in chapter_stats[:3]:  # Print first 3 chapters as sample
            print(f"    - [{stat['ch_id']}] {stat['title']}: {stat['block_count']} resources ({stat['content_types']})")
        if len(chapter_stats) > 3:
            print(f"    - ... and {len(chapter_stats) - 3} more chapters")
        print("-" * 74)

if __name__ == "__main__":
    audit_dashboard_counts()
