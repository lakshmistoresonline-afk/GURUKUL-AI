import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def verify_maths_fusion():
    print("==========================================================================")
    print("DEEP FORENSIC VERIFICATION OF ALL 5 MATHS JSON FILES FUSION")
    print("==========================================================================\n")

    meta = ContentLoaderService.get_subject_curriculum_metadata("5", "Maths")
    units = meta.get("units", [])
    print(f"Total Maths Units Discovered: {len(units)}")

    total_chapters = 0
    total_blocks = 0
    total_flashcards = 0
    total_quizzes = 0
    total_mcqs = 0
    total_sas = 0

    for u in units:
        u_num = u.get("unitNumber", 1)
        for ch in u.get("chapters", []):
            ch_num = ch.get("chapterNumber", 1)
            ch_id = ch.get("id") or f"G5-MAT-U{u_num:02d}-C{ch_num:02d}"

            ch_source = ContentLoaderService.load_chapter_source("5", "Maths", ch_id)
            adapter = AdapterResolver.resolve("NCERT", "5", "Maths", ch_source)
            blocks = adapter.parse_chapter(ch_source, ch_id)

            total_chapters += 1
            total_blocks += len(blocks)

            # Check individual blocks
            f_b = next((b for b in blocks if b.normalizedType == "flashcards"), None)
            f_count = len(f_b.data) if f_b and isinstance(f_b.data, list) else 0

            q_b = next((b for b in blocks if b.normalizedType == "quiz"), None)
            q_count = len(q_b.data) if q_b and isinstance(q_b.data, list) else 0

            sq_b = next((b for b in blocks if b.normalizedType == "studyQuestions"), None)
            sq_d = sq_b.data if sq_b and isinstance(sq_b.data, dict) else {}
            mcq_c = len(sq_d.get("multipleChoiceQuestions", []))
            sa_c = len(sq_d.get("shortAnswerQuestions", []))

            total_flashcards += f_count
            total_quizzes += q_count
            total_mcqs += mcq_c
            total_sas += sa_c

            block_renderers = [b.renderer for b in blocks]

            print(f"  Ch {ch_num:02d} ({ch_id}): '{ch_source.get('chapterTitle')}' | Blocks: {len(blocks)} {block_renderers} | Flashcards: {f_count:2d} | Quiz Qs: {q_count:2d} | Practice MCQs: {mcq_c:2d} | SAs: {sa_c:2d}")

    print("\n==========================================================================")
    print(f"MATHS 5-FILE FUSION SUMMARY:")
    print(f"  Total Chapters: {total_chapters} / 15")
    print(f"  Total ContentBlocks Parsed: {total_blocks}")
    print(f"  Total Flashcards: {total_flashcards} (Expected: 300)")
    print(f"  Total Quiz Questions: {total_quizzes} (Expected: 375)")
    print(f"  Total Practice MCQs: {total_mcqs}")
    print(f"  Total Practice Short Answers: {total_sas}")
    print("==========================================================================")

if __name__ == "__main__":
    verify_maths_fusion()
