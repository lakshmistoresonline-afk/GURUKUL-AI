import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def audit_study_questions():
    subjects = ["English", "Hindi", "Maths", "Science"]
    print("==========================================================================")
    print("FORENSIC STUDY QUESTIONS AUDIT ACROSS ALL 47 CHAPTERS")
    print("==========================================================================\n")

    for sub in subjects:
        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        units = meta.get("units", [])
        print(f"SUBJECT: Class 5 {sub}")

        for u in units:
            chs = u.get("chapters", [])
            for ch in chs:
                ch_id = ch.get("id")
                ch_source = ContentLoaderService.load_chapter_source("5", sub, ch_id)
                adapter = AdapterResolver.resolve("NCERT", "5", sub, ch_source)
                blocks = adapter.parse_chapter(ch_source, ch_id)

                sq_block = next((b for b in blocks if b.normalizedType == "studyQuestions" or b.sourceType == "studyQuestions"), None)
                if sq_block:
                    sq_data = sq_block.data
                    if isinstance(sq_data, dict):
                        mcqs = sq_data.get("multipleChoiceQuestions", [])
                        sas = sq_data.get("shortAnswerQuestions", [])

                        # Inspect key types in sas
                        sa_keys = set()
                        for item in sas:
                            if isinstance(item, dict):
                                sa_keys.update(item.keys())
                            elif isinstance(item, str):
                                sa_keys.add("STRING_ITEM")

                        print(f"  Ch {ch.get('chapterNumber'):02d} ({ch_id}): {len(mcqs)} MCQs | {len(sas)} SAs -> SA Keys: {sorted(list(sa_keys))}")

        print("-" * 74)

if __name__ == "__main__":
    audit_study_questions()
