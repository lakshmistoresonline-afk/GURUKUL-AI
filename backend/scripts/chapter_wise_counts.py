import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

def generate_chapter_counts():
    files = ContentLoaderService.load_raw_subject_files("5", "English")
    notes = files.get("santoor_chapters_notes.json", {}).get("chapters", [])
    flash_data = files.get("santoor_flashcards.json", {}).get("cards", [])
    quiz_data = files.get("santoor_quiz.json", {}).get("questions", [])
    mm_data = files.get("santoor_mindmap.json", {}).get("units", [])

    print("=== CHAPTER-WISE DATA RECORD COUNTS ===\n")
    print(f"{'Ch ID':<15} | {'Title':<28} | {'Terms':<6} | {'Breakdown':<10} | {'Takeaways':<10} | {'Study MCQ':<10} | {'Study SA':<9} | {'Study Ref':<10} | {'Total Practice':<14} | {'Flashcards':<10} | {'Quiz':<5} | {'Mindmap':<8} | {'Total Blocks':<12}")
    print("-" * 155)

    tot_terms = 0
    tot_bd = 0
    tot_tk = 0
    tot_mcq = 0
    tot_sa = 0
    tot_rf = 0
    tot_flash = 0
    tot_quiz = 0
    tot_mm = 0
    tot_blocks = 0

    for c in notes:
        u = c["unitNumber"]
        ch = c["chapterNumber"]
        ch_id = f"G5-ENG-U{u:02d}-C{ch:02d}"
        title = c["chapterTitle"]

        # Terms count
        terms_count = len(c.get("keyTerminology", []))
        tot_terms += terms_count

        # Breakdown count
        bd_count = len(c.get("detailedBreakdown", []))
        tot_bd += bd_count

        # Takeaways count
        tk_count = len(c.get("importantTakeaways", []))
        tot_tk += tk_count

        # Study Questions count
        sq = c.get("studyQuestions", {})
        mcq_count = len(sq.get("multipleChoiceQuestions", []))
        sa_count = len(sq.get("shortAnswerQuestions", []))
        rf_count = len(sq.get("reflectionQuestions", []))
        sq_total = mcq_count + sa_count + rf_count

        tot_mcq += mcq_count
        tot_sa += sa_count
        tot_rf += rf_count

        # Flashcards count for this chapter
        flash_count = len([f for f in flash_data if f.get("unit") == u and f.get("chapter") == ch])
        tot_flash += flash_count

        # Quiz count for this chapter
        quiz_count = len([q for q in quiz_data if q.get("unit") == u and q.get("chapter") == ch])
        tot_quiz += quiz_count

        # Mindmap
        mm_present = 0
        for u_obj in mm_data:
            if u_obj.get("unitNumber") == u:
                for c_obj in u_obj.get("chapters", []):
                    if c_obj.get("chapterNumber") == ch:
                        mm_present = 1
                        break
        tot_mm += mm_present

        blocks_count = 8  # 8 ContentBlocks per chapter

        tot_blocks += blocks_count

        print(f"{ch_id:<15} | {title:<28} | {terms_count:<6} | {bd_count:<10} | {tk_count:<10} | {mcq_count:<10} | {sa_count:<9} | {rf_count:<10} | {sq_total:<14} | {flash_count:<10} | {quiz_count:<5} | {mm_present:<8} | {blocks_count:<12}")

    print("-" * 155)
    print(f"{'TOTALS':<15} | {'10 Chapters':<28} | {tot_terms:<6} | {tot_bd:<10} | {tot_tk:<10} | {tot_mcq:<10} | {tot_sa:<9} | {tot_rf:<10} | {tot_mcq+tot_sa+tot_rf:<14} | {tot_flash:<10} | {tot_quiz:<5} | {tot_mm:<8} | {tot_blocks:<12}")

if __name__ == "__main__":
    generate_chapter_counts()
