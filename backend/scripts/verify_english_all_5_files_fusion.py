import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def verify_english_fusion():
    print("==========================================================================")
    print("DEEP FORENSIC VERIFICATION OF ALL 5 ENGLISH JSON FILES FUSION")
    print("==========================================================================\n")

    meta = ContentLoaderService.get_subject_curriculum_metadata("5", "English")
    units = meta.get("units", [])
    print(f"Total English Units Discovered: {len(units)}")

    total_chapters = 0
    total_blocks = 0
    total_flashcards = 0
    total_quizzes = 0

    for u in units:
        u_num = u.get("unitNumber", 1)
        for ch in u.get("chapters", []):
            ch_num = ch.get("chapterNumber", 1)
            ch_id = ch.get("id") or f"G5-ENG-U{u_num:02d}-C{ch_num:02d}"

            ch_source = ContentLoaderService.load_chapter_source("5", "English", ch_id)
            adapter = AdapterResolver.resolve("NCERT", "5", "English", ch_source)
            blocks = adapter.parse_chapter(ch_source, ch_id)

            total_chapters += 1
            total_blocks += len(blocks)

            f_b = next((b for b in blocks if b.normalizedType == "flashcards"), None)
            f_count = len(f_b.data) if f_b and isinstance(f_b.data, list) else 0

            q_b = next((b for b in blocks if b.normalizedType == "quiz"), None)
            q_count = len(q_b.data) if q_b and isinstance(q_b.data, list) else 0

            total_flashcards += f_count
            total_quizzes += q_count

            print(f"  Ch {ch_num:02d} ({ch_id}): '{ch_source.get('chapterTitle')}' | Blocks: {len(blocks)} | Flashcards: {f_count:2d} | Quiz Qs: {q_count:2d}")

    print("\n==========================================================================")
    print(f"ENGLISH 5-FILE FUSION SUMMARY:")
    print(f"  Total Chapters: {total_chapters} / 10")
    print(f"  Total ContentBlocks Parsed: {total_blocks}")
    print(f"  Total Flashcards: {total_flashcards}")
    print(f"  Total Quiz Questions: {total_quizzes}")
    print("==========================================================================")

if __name__ == "__main__":
    verify_english_fusion()
