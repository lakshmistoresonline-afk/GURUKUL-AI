import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def verify_all_47_chapters():
    subjects = ["English", "Hindi", "Maths", "Science"]
    print("==========================================================================")
    print("FORENSIC 47-CHAPTER DATA & RENDERING VERIFICATION (CLASS 5)")
    print("==========================================================================\n")

    total_chapters = 0
    total_blocks = 0
    issues_found = []

    for sub in subjects:
        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        units = meta.get("units", [])

        print(f"SUBJECT: Class 5 {sub} (Units: {len(units)})")
        for u in units:
            u_num = u.get("unitNumber", 1)
            chs = u.get("chapters", [])
            for ch in chs:
                ch_num = ch.get("chapterNumber", 1)
                ch_id = ch.get("id") or f"G5-{sub[:3].upper()}-U{u_num:02d}-C{ch_num:02d}"
                ch_title = ch.get("title", "")

                ch_source = ContentLoaderService.load_chapter_source("5", sub, ch_id)
                if not ch_source:
                    issues_found.append(f"Missing source data for {sub} {ch_id}")
                    continue

                adapter = AdapterResolver.resolve("NCERT", "5", sub, ch_source)
                blocks = adapter.parse_chapter(ch_source, ch_id)

                total_chapters += 1
                total_blocks += len(blocks)

                # Check for duplicate block IDs
                block_ids = [b.id for b in blocks]
                if len(block_ids) != len(set(block_ids)):
                    issues_found.append(f"Duplicate ContentBlock IDs in {sub} {ch_id}")

                # Check for unassigned renderers
                for b in blocks:
                    if not b.renderer or b.renderer == "unknown":
                        issues_found.append(f"Unassigned renderer for {sub} {ch_id} block '{b.sourceType}'")

                print(f"  Ch {ch_num:02d} ({ch_title:<35}): {len(blocks):2d} ContentBlocks | {len(ch_source):2d} Source Keys")

        print("-" * 74)

    print(f"\nAUDIT SUMMARY:")
    print(f"  Total Chapters Verified: {total_chapters} / 47")
    print(f"  Total Normalized ContentBlocks Generated: {total_blocks}")
    print(f"  Total Issues Found: {len(issues_found)}")

    if issues_found:
        print("\nISSUES DETECTED:")
        for issue in issues_found:
            print(f"  - {issue}")
    else:
        print("\nSUCCESS: ZERO ISSUES DETECTED ACROSS ALL 47 CHAPTERS IN ALL 4 SUBJECTS!")

if __name__ == "__main__":
    verify_all_47_chapters()
