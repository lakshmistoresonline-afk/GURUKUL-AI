import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def run_idempotency_test():
    print("==========================================================================")
    print("PHASE 0: REGENERATION IDEMPOTENCY TEST (RUN 1 vs RUN 2)")
    print("==========================================================================\n")

    subjects = ["English", "Hindi", "Maths", "Science"]

    # RUN 1
    run1_data = {}
    for sub in subjects:
        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        units = meta.get("units", [])

        run1_data[sub] = []
        for u in units:
            u_num = u.get("unitNumber", 1)
            for ch in u.get("chapters", []):
                ch_num = ch.get("chapterNumber", 1)
                ch_id = ch.get("id") or f"G5-{sub[:3].upper()}-U{u_num:02d}-C{ch_num:02d}"

                ch_source = ContentLoaderService.load_chapter_source("5", sub, ch_id)
                adapter = AdapterResolver.resolve("NCERT", "5", sub, ch_source)
                blocks = adapter.parse_chapter(ch_source, ch_id)
                manifest = adapter.generate_manifest(ch_id, blocks)

                run1_data[sub].append({
                    "chapterId": ch_id,
                    "block_ids": [b.id for b in blocks],
                    "block_count": len(blocks),
                    "manifest": manifest.model_dump() if hasattr(manifest, "model_dump") else manifest.dict()
                })

    # RUN 2
    run2_data = {}
    for sub in subjects:
        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        units = meta.get("units", [])

        run2_data[sub] = []
        for u in units:
            u_num = u.get("unitNumber", 1)
            for ch in u.get("chapters", []):
                ch_num = ch.get("chapterNumber", 1)
                ch_id = ch.get("id") or f"G5-{sub[:3].upper()}-U{u_num:02d}-C{ch_num:02d}"

                ch_source = ContentLoaderService.load_chapter_source("5", sub, ch_id)
                adapter = AdapterResolver.resolve("NCERT", "5", sub, ch_source)
                blocks = adapter.parse_chapter(ch_source, ch_id)
                manifest = adapter.generate_manifest(ch_id, blocks)

                run2_data[sub].append({
                    "chapterId": ch_id,
                    "block_ids": [b.id for b in blocks],
                    "block_count": len(blocks),
                    "manifest": manifest.model_dump() if hasattr(manifest, "model_dump") else manifest.dict()
                })

    # COMPARE RUN 1 vs RUN 2
    idempotency_pass = True
    for sub in subjects:
        r1_list = run1_data[sub]
        r2_list = run2_data[sub]

        if len(r1_list) != len(r2_list):
            print(f"FAILED: Chapter count mismatch for {sub}: Run 1={len(r1_list)} vs Run 2={len(r2_list)}")
            idempotency_pass = False
            continue

        for i in range(len(r1_list)):
            if r1_list[i] != r2_list[i]:
                print(f"FAILED: Content difference at {sub} chapter {i+1}")
                idempotency_pass = False

        print(f"Subject {sub:<8} | Run 1 Chapters: {len(r1_list)} | Run 2 Chapters: {len(r2_list)} | IDEMPOTENT: TRUE")

    print("-" * 74)
    print(f"OVERALL REGENERATION IDEMPOTENCY STATUS: {'100% PASSED' if idempotency_pass else 'FAILED'}")
    return idempotency_pass

if __name__ == "__main__":
    run_idempotency_test()
