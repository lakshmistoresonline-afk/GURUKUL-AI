import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def test_all_subjects():
    grades = ContentLoaderService.discover_grades()
    print("==========================================================================")
    print("MASTER INGESTION & NORMALIZATION TEST ACROSS ALL SUBJECTS")
    print("==========================================================================\n")
    print(f"Discovered Grades: {grades}")

    for g in grades:
        subjects = ContentLoaderService.discover_subjects(g)
        print(f"\nGrade Class {g} Subjects Discovered: {subjects}")

        for sub in subjects:
            meta = ContentLoaderService.get_subject_curriculum_metadata(g, sub)
            print(f"\nSubject: Class {g} {sub}")
            print(f"  Framework: {meta.get('curriculumFramework')}")

            # Load Chapter 1
            ch_data = ContentLoaderService.load_chapter_source(g, sub, f"G{g}-{sub[:3].upper()}-U01-C01")
            if ch_data:
                adapter = AdapterResolver.resolve("NCERT", g, sub, ch_data)
                blocks = adapter.parse_chapter(ch_data, f"G{g}-{sub[:3].upper()}-U01-C01")
                manifest = adapter.generate_manifest(f"G{g}-{sub[:3].upper()}-U01-C01", blocks)

                print(f"  Chapter 1 Title: {ch_data.get('chapterTitle') or ch_data.get('chapter_title')}")
                print(f"  Adapter Resolved: {type(adapter).__name__}")
                print(f"  Normalized ContentBlocks Count: {len(blocks)}")
                print(f"  Manifest Content Types: {[item.type for item in manifest.contentTypes]}")

if __name__ == "__main__":
    test_all_subjects()
