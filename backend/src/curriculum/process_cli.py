import os
import json
import argparse
from datetime import datetime

CONTENTS_ROOT = r"D:\GURUKUL\Contents"
PROCESSED_ROOT = r"D:\GURUKUL\ProcessedContent"

def diversify_question_sets(qp_papers, chapter_overview):
    concepts = chapter_overview.get("key_concepts", []) or chapter_overview.get("learningObjectives", [])
    if not qp_papers:
        return

    for s_idx, paper in enumerate(qp_papers):
        if s_idx == 0:
            continue

        # Customize paper title for distinction
        orig_title = paper.get("paper_title", f"Set {s_idx + 1} Practice Paper")
        if f"Set {s_idx + 1}" not in orig_title:
            paper["paper_title"] = f"Set {s_idx + 1} - Advanced Practice Assessment"

        for sec in paper.get("sections", []):
            for q_idx, q in enumerate(sec.get("questions", [])):
                q_text = q.get("question_text", "")
                if concepts and (q_idx < len(concepts)):
                    concept_hint = concepts[q_idx % len(concepts)]
                    if isinstance(concept_hint, str):
                        q["question_text"] = f"[Set {s_idx + 1} Analytical Variant] Considering {concept_hint.split(':')[0]} — {q_text}"

                # Diversify options for higher sets
                options = q.get("options", [])
                if len(options) >= 4:
                    shift = s_idx % len(options)
                    q["options"] = options[shift:] + options[:shift]

def process_subject(grade: str, subject: str):
    subj_dir = os.path.join(CONTENTS_ROOT, f"Class {grade}", subject)
    if not os.path.exists(subj_dir):
        print(f"Skipping Class {grade} {subject}: directory not found at {subj_dir}")
        return

    print(f"Processing Grade {grade} Subject: {subject}...")

    files = {}
    for f in os.listdir(subj_dir):
        if f.lower().endswith(".json"):
            path = os.path.join(subj_dir, f)
            try:
                with open(path, "r", encoding="utf-8") as file:
                    files[f] = json.load(file)
            except Exception as e:
                print(f"  Error loading {f}: {e}")

    ov_data = None
    for k, v in files.items():
        if "overview" in k.lower() and isinstance(v, dict) and "chapters" in v:
            ov_data = v
            break
    if not ov_data:
        for k, v in files.items():
            if isinstance(v, dict) and "chapters" in v:
                ov_data = v
                break

    if not ov_data or "chapters" not in ov_data:
        print(f"  Warning: No chapters found for Class {grade} {subject}")
        return

    chapters = ov_data.get("chapters", [])
    sub_processed_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject.replace(" ", ""))
    os.makedirs(sub_processed_dir, exist_ok=True)

    subject_code = subject.replace(" ", "").upper()[:3]
    chapters_processed = 0

    for idx, ch in enumerate(chapters):
        try:
            c_num = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("chapter_no") or (idx + 1)
            ch_id = f"G{grade}-{subject_code}-U01-C{c_num:02d}"
            ch_dir = os.path.join(sub_processed_dir, ch_id)
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

            # Question Papers (Merge and Diversify Sets)
            qp_papers = []
            for k, v in files.items():
                if "question" in k.lower() and "paper" in k.lower() and isinstance(v, dict):
                    qp_list = v.get("chapters", [])
                    if isinstance(qp_list, list):
                        for i, qpc in enumerate(qp_list):
                            if match_ch(qpc, i):
                                p_list = qpc.get("question_papers", []) or qpc.get("papers", [])
                                qp_papers.extend(p_list)

            if qp_papers:
                diversify_question_sets(qp_papers, ch)
                sections["question_papers"] = {
                    "chapter_number": c_num,
                    "chapter_title": ch.get("chapter_title", ch_id),
                    "question_papers": qp_papers
                }

            for sec_name, sec_data in sections.items():
                sec_path = os.path.join(ch_dir, f"{sec_name}.json")
                with open(sec_path, "w", encoding="utf-8") as f:
                    json.dump(sec_data, f, ensure_ascii=False, indent=2)

            manifest = {
                "meta": {
                    "class": int(grade),
                    "subject": subject,
                    "chapter_id": ch_id,
                    "schema_version": "1.0",
                    "processor_version": f"class{grade}-{subject.lower()}-v1",
                    "processed_at": datetime.utcnow().isoformat() + "Z",
                    "status": "ready"
                },
                "sectionsPresent": list(sections.keys())
            }
            manifest_path = os.path.join(ch_dir, "manifest.json")
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)

            chapters_processed += 1
        except Exception as e:
            print(f"  [ERROR] Failed to process chapter {ch_id}: {e}")

    print(f"Completed {subject}: {chapters_processed} chapters processed into {sub_processed_dir}")

def main():
    parser = argparse.ArgumentParser(description="Gurukul AI Persistent Processed Data Layer CLI")
    parser.add_argument("--class", dest="grade", type=str, default="5")
    parser.add_argument("--subject", type=str, default=None)
    args = parser.parse_args()

    os.makedirs(PROCESSED_ROOT, exist_ok=True)

    if args.subject:
        process_subject(args.grade, args.subject)
    else:
        for subj in ["English", "Hindi", "Maths", "Science"]:
            process_subject(args.grade, subj)

    print("\nALL PERSISTENT PROCESSED DATA GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
