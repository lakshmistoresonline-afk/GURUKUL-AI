import os
import json
from datetime import datetime

CONTENTS_ROOT = r"D:\GURUKUL\Contents\Class 7"
PROCESSED_ROOT = r"D:\GURUKUL\ProcessedContent\Class7"

SUBJECTS = ["English", "Hindi", "Maths I", "Maths II", "Science", "Social I", "Social II"]

def process_class7():
    print("==========================================================================")
    print("PROCESSING CLASS 7 CURRICULUM PIPELINE (NEP 2020 & NCF-SE 2023)")
    print("==========================================================================\n")

    os.makedirs(PROCESSED_ROOT, exist_ok=True)

    total_chapters_processed = 0

    for subject in SUBJECTS:
        subj_dir = os.path.join(CONTENTS_ROOT, subject)
        if not os.path.exists(subj_dir):
            print(f"Skipping {subject}: directory not found.")
            continue

        print(f"Processing Class 7 Subject: {subject}...")

        files = {}
        for f in os.listdir(subj_dir):
            if f.lower().endswith(".json"):
                path = os.path.join(subj_dir, f)
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        files[f] = json.load(file)
                except Exception as e:
                    print(f"  Error loading {f}: {e}")

        # Extract chapters from Overview.json or Notes.json
        ov_data = None
        for k, v in files.items():
            if "overview" in k.lower() and isinstance(v, dict):
                ov_data = v
                break

        if not ov_data:
            for k, v in files.items():
                if isinstance(v, dict) and "chapters" in v:
                    ov_data = v
                    break

        if not ov_data or "chapters" not in ov_data:
            print(f"  Warning: No chapters found for {subject}")
            continue

        chapters = ov_data.get("chapters", [])
        subj_processed_dir = os.path.join(PROCESSED_ROOT, subject.replace(" ", ""))
        os.makedirs(subj_processed_dir, exist_ok=True)

        subject_code = subject.replace(" ", "").upper()[:3]

        for idx, ch in enumerate(chapters):
            c_num = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("chapter_no") or (idx + 1)
            ch_id = f"G7-{subject_code}-U01-C{c_num:02d}"
            ch_dir = os.path.join(subj_processed_dir, ch_id)
            os.makedirs(ch_dir, exist_ok=True)

            sections = {
                "overview": ch,
                "notes": None,
                "master": None,
                "flashcards": [],
                "mindmaps": {},
                "quiz": [],
                "question_papers": None
            }

            def match_ch(item: dict, i: int) -> bool:
                c = item.get("chapter_number") or item.get("chapterNumber") or item.get("chapter_no") or item.get("chapter") or (i + 1)
                return c == c_num or f"C{c:02d}" in ch_id

            # Notes
            for k, v in files.items():
                if "notes" in k.lower() and isinstance(v, dict):
                    n_list = v.get("chapters", []) if "chapters" in v else v
                    if isinstance(n_list, list):
                        for i, nc in enumerate(n_list):
                            if match_ch(nc, i):
                                sections["notes"] = nc
                                break

            # Master
            for k, v in files.items():
                if "master" in k.lower() and isinstance(v, dict):
                    m_list = v.get("chapters", []) if "chapters" in v else v
                    if isinstance(m_list, list):
                        for i, mc in enumerate(m_list):
                            if match_ch(mc, i):
                                sections["master"] = mc
                                break

            # Flashcards
            for k, v in files.items():
                if "flashcard" in k.lower() and isinstance(v, dict):
                    fc_list = v.get("chapters", []) or v.get("flashcards", []) or v.get("flashcards_dataset", [])
                    if isinstance(fc_list, list):
                        for i, fcc in enumerate(fc_list):
                            if match_ch(fcc, i):
                                sections["flashcards"] = fcc.get("flashcards", []) or fcc.get("cards", []) or []
                                break
                        if not sections["flashcards"]:
                            for fcc in fc_list:
                                if isinstance(fcc, dict) and ("front" in fcc or "front_prompt" in fcc or "front_question" in fcc or "term" in fcc):
                                    sections["flashcards"].append(fcc)

            # Mindmaps
            for k, v in files.items():
                if "mindmap" in k.lower() and isinstance(v, dict):
                    mm_list = v.get("chapters", []) or v.get("mindmaps_dataset", [])
                    if isinstance(mm_list, list):
                        for i, mm in enumerate(mm_list):
                            if match_ch(mm, i):
                                sections["mindmaps"] = mm.get("mind_map", mm.get("mindmap", mm))
                                break
                        if not sections["mindmaps"] and len(mm_list) >= c_num:
                            mm_item = mm_list[c_num - 1]
                            sections["mindmaps"] = mm_item.get("mind_map", mm_item.get("mindmap", mm_item))

            # Quiz
            for k, v in files.items():
                if "quiz" in k.lower() and isinstance(v, dict):
                    qz_list = v.get("chapters", []) or v.get("quiz_dataset", [])
                    if isinstance(qz_list, list):
                        for i, qz in enumerate(qz_list):
                            if match_ch(qz, i):
                                sections["quiz"] = qz.get("quizzes", []) or qz.get("questions", []) or qz.get("quiz", [])
                                break
                        if not sections["quiz"] and len(qz_list) >= c_num:
                            ch_qz = qz_list[c_num - 1]
                            sections["quiz"] = ch_qz.get("quizzes", []) or ch_qz.get("questions", []) or ch_qz.get("quiz", [])

            # Question Papers
            for k, v in files.items():
                if "question" in k.lower() and isinstance(v, dict):
                    qp_list = v.get("chapters", [])
                    if isinstance(qp_list, list):
                        for i, qpc in enumerate(qp_list):
                            if match_ch(qpc, i):
                                sections["question_papers"] = qpc
                                break

            # Write individual section files
            for sec_name, sec_val in sections.items():
                sec_path = os.path.join(ch_dir, f"{sec_name}.json")
                with open(sec_path, "w", encoding="utf-8") as sf:
                    json.dump(sec_val, sf, ensure_ascii=False, indent=2)

            total_chapters_processed += 1

        print(f"  Completed Class 7 {subject}: {len(chapters)} chapters processed into {subj_processed_dir}")

    print(f"\nCLASS 7 MULTI-BOOK CURRICULUM PIPELINE COMPLETED SUCCESSFULLY! Total Chapters: {total_chapters_processed}")

if __name__ == "__main__":
    process_class7()
