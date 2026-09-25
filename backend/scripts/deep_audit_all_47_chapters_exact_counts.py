import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def deep_audit_exact_counts():
    subjects = ["English", "Hindi", "Maths", "Science"]
    print("==========================================================================")
    print("DEEP FORENSIC EXACT ITEM COUNTS AUDIT ACROSS ALL 47 CHAPTERS")
    print("==========================================================================\n")

    grand_total_flashcards = 0
    grand_total_quiz_qs = 0
    grand_total_blocks = 0

    for sub in subjects:
        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        units = meta.get("units", [])
        sub_flash = 0
        sub_quiz = 0
        sub_blocks = 0

        print(f"================ SUBJECT: Class 5 {sub} ================")

        for u in units:
            u_num = u.get("unitNumber", 1)
            for ch in u.get("chapters", []):
                ch_num = ch.get("chapterNumber", 1)
                ch_id = ch.get("id") or f"G5-{sub[:3].upper()}-U{u_num:02d}-C{ch_num:02d}"

                ch_source = ContentLoaderService.load_chapter_source("5", sub, ch_id)
                adapter = AdapterResolver.resolve("NCERT", "5", sub, ch_source)
                blocks = adapter.parse_chapter(ch_source, ch_id)

                # Count flashcards block
                flash_block = next((b for b in blocks if b.normalizedType == "flashcards"), None)
                flash_count = len(flash_block.data) if flash_block and isinstance(flash_block.data, list) else 0

                # Count quiz block
                quiz_block = next((b for b in blocks if b.normalizedType == "quiz"), None)
                quiz_count = len(quiz_block.data) if quiz_block and isinstance(quiz_block.data, list) else 0

                # Count practice questions block
                sq_block = next((b for b in blocks if b.normalizedType == "studyQuestions"), None)
                sq_data = sq_block.data if sq_block and isinstance(sq_block.data, dict) else {}
                mcq_count = len(sq_data.get("multipleChoiceQuestions", []))
                sa_count = len(sq_data.get("shortAnswerQuestions", []))

                sub_flash += flash_count
                sub_quiz += quiz_count
                sub_blocks += len(blocks)

                print(f"  Ch {ch_num:02d} ({ch_id}): {len(blocks):2d} Blocks | {flash_count:2d} Flashcards | {quiz_count:2d} Quiz Questions | Practice MCQs: {mcq_count:2d} | Practice SAs: {sa_count:2d}")

        print(f"SUBTOTAL {sub}: {len(units)} Units | {sub_blocks} Blocks | {sub_flash} Flashcards | {sub_quiz} Quiz Questions\n")
        grand_total_flashcards += sub_flash
        grand_total_quiz_qs += sub_quiz
        grand_total_blocks += sub_blocks

    print("==========================================================================")
    print(f"GRAND TOTALS ACROSS ALL 47 CHAPTERS:")
    print(f"  Total ContentBlocks Parsed: {grand_total_blocks}")
    print(f"  Total Flashcards Showcased: {grand_total_flashcards}")
    print(f"  Total Quiz Questions Showcased: {grand_total_quiz_qs}")
    print("==========================================================================")

if __name__ == "__main__":
    deep_audit_exact_counts()
