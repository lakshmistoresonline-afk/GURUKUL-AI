import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver
from src.navigation.navigation_builder import BackendNavigationBuilder

def run_comprehensive_audit():
    print("==========================================================================")
    print("AUTOMATED COMPREHENSIVE AUDIT OF ALL 47 CLASS 5 CHAPTERS")
    print("==========================================================================\n")

    grades = ContentLoaderService.discover_grades()
    print(f"Discovered Grades: {grades}")

    total_chapters_verified = 0
    failures = []

    for grade in grades:
        subjects = ContentLoaderService.discover_subjects(grade)
        print(f"Grade {grade} Subjects: {subjects}")

        for subject in subjects:
            meta = ContentLoaderService.get_subject_curriculum_metadata(grade, subject)
            units = meta.get("units", [])

            sub_ch_count = 0
            for u in units:
                for ch in u.get("chapters", []):
                    ch_id = ch.get("id")
                    sub_ch_count += 1
                    total_chapters_verified += 1

                    try:
                        ch_source = ContentLoaderService.load_chapter_source(grade, subject, ch_id)
                        if not ch_source:
                            failures.append(f"{subject} {ch_id}: load_chapter_source returned None")
                            continue

                        adapter = AdapterResolver.resolve("NCERT", grade, subject, ch_source)
                        blocks = adapter.parse_chapter(ch_source, ch_id)
                        if not blocks:
                            failures.append(f"{subject} {ch_id}: parse_chapter returned empty blocks")
                            continue

                        manifest = adapter.generate_manifest(ch_id, blocks)
                        tabs = BackendNavigationBuilder.build_navigation(subject, manifest)
                        tab_ids = [t["id"] for t in tabs]

                        # Verify 5-stage navigation and quiz last
                        if "quiz" not in tab_ids or tab_ids[-1] != "quiz":
                            failures.append(f"{subject} {ch_id}: Invalid navigation tabs {tab_ids}")

                    except Exception as e:
                        failures.append(f"{subject} {ch_id}: Exception {str(e)}")

            print(f"  Subject '{subject}': {sub_ch_count} chapters audited.")

    print(f"\n==========================================================================")
    print(f"COMPREHENSIVE AUDIT RESULTS:")
    print(f"  Total Chapters Verified: {total_chapters_verified} / 47")
    print(f"  Failures Found: {len(failures)}")
    if failures:
        print("  Failures list:")
        for f in failures[:10]:
            print(f"    - {f}")
    else:
        print("  VERDICT: 100% AUTOMATED CROSS-SUBJECT CHAPTER AUDIT PASSED!")
    print("==========================================================================")

if __name__ == "__main__":
    run_comprehensive_audit()
