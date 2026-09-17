import os
import json
import hashlib
import re
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path("D:/GURUKUL-AI")
CONTENTS_ROOT = PROJECT_ROOT / "Contents" / "Class 5"
RUNTIME_ROOT = PROJECT_ROOT / "runtime-data"
CHAPTERS_OUT = RUNTIME_ROOT / "chapters"

# REJECTION RULES: Content fragments that should never be student-facing cards
REJECT_PATTERNS = [
    r'^\d+\.?$', # Isolated numbers
    r'^[a-z]\.?$', # Isolated letters
    r'^\(?[i|v|x]+\)?\.?$', # Roman numerals
    r'^\?$', # Isolated punctuation
    r'^Chapter \d+\.indd.*$',
    r'^Reprint \d{4}-\d{2}$',
    r'.*Santoor Grade 5.*',
    r'.*Papa.s Spectacles.*',
    r'.*Gone with the Scooter.*',
    r'.*The Rainbow.*',
    r'.*The Wise Parrot.*',
    r'.*The Frog.*',
    r'.*What a Tank.*',
    r'.*Gilli Danda.*'
]

def clean_text(text: str) -> str:
    if not text: return ""
    # Standardize encoding
    text = text.replace('â', "'").replace('â', '"').replace('â', '"').replace('â', "-").replace('â', " ")

    # Remove obvious OCR/Document artifacts line-by-line
    lines = text.splitlines()
    cleaned_lines = []
    for l in lines:
        l = l.strip()
        if any(re.match(p, l, re.IGNORECASE) for p in REJECT_PATTERNS):
            continue
        cleaned_lines.append(l)

    cleaned = "\n".join(cleaned_lines)
    # Collapse multiple newlines
    cleaned = re.sub(r'\n{3,}', "\n\n", cleaned).strip()
    return cleaned

def normalize_for_dedup(text: str) -> str:
    if not text: return ""
    # Remove all non-alphanumeric for a very aggressive dupe check
    return re.sub(r'[^a-z0-9]', "", text.lower())

def semantic_split(text: str) -> List[str]:
    cleaned = clean_text(text)
    if not cleaned: return []
    # Split on double newline
    blocks = re.split(r'\n\s*\n', cleaned)
    return [b.strip() for b in blocks if len(b.strip()) > 2]

def detect_type(text: str, current_type: str = "paragraph") -> str:
    if not text: return current_type
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines: return current_type

    # Dialogue
    if all(":" in l and len(l.split(":")[0]) < 25 for l in lines) and len(lines) > 1:
        return "dialogue"

    # Poem
    if len(lines) >= 3 and all(len(l) < 70 for l in lines) and not any(":" in l for l in lines):
        return "poem"

    # Heading
    if len(text.split()) < 10 and not text.endswith((".", "?", "!")):
        if text[0].isupper() or text.startswith("Let us"):
            return "heading"

    # Question
    if text.startswith(("Q.", "Q1", "Q2", "Q3", "1.", "2.", "A.", "B.", "C.")) or "?" in text:
        return "question"

    return current_type

def get_deterministic_id(class_id, subject, chapter, pillar, text, seq) -> str:
    content_hash = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]
    return f"class05_{subject.lower()}_{chapter}_{pillar}_{seq}_{content_hash}"

class Class5Adapter:
    def __init__(self):
        self.catalog = {"classes": []}
        self.search_index = []

    def find_chapter_dirs(self, root: Path) -> List[Path]:
        chapters = []
        for p in root.rglob("01_LEARN"):
            if p.is_dir(): chapters.append(p.parent)
        return sorted(list(set(chapters)), key=lambda x: x.name)

    def process_all(self):
        class_summary = {"id": "class_5", "name": "Class 5", "subjects": []}
        subjects = sorted([d for d in CONTENTS_ROOT.iterdir() if d.is_dir()])

        for subj_dir in subjects:
            subj_name = subj_dir.name
            display_subj_name = subj_name.replace("_COMPLETE", "")
            subj_id = f"class_5_{display_subj_name.lower()}"

            chapters = self.find_chapter_dirs(subj_dir)
            if not chapters: continue

            subject_summary = {"id": subj_id, "name": display_subj_name, "chapters": []}

            for ch_dir in chapters:
                try:
                    ch_data = self.process_chapter(ch_dir, subj_id, display_subj_name)
                    subject_summary["chapters"].append({
                        "id": ch_data["id"], "chapter_id": ch_data["chapter_id"],
                        "title": ch_data["title"], "counts": ch_data["counts"]
                    })

                    out_path = CHAPTERS_OUT / "Class 5" / display_subj_name / f"{ch_data['chapter_id']}.json"
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(out_path, "w", encoding="utf-8") as f:
                        json.dump(ch_data, f, indent=2, ensure_ascii=False)

                    for layer in ["learn", "practice", "assess", "revise"]:
                        for block in ch_data.get(layer, []):
                            self.search_index.append({
                                "id": block["id"], "class": "Class 5", "subject": display_subj_name,
                                "chapter": ch_data["title"], "chapter_id": ch_data["id"],
                                "layer": layer, "title": block.get("title") or "", "text": block.get("text") or ""
                            })
                except Exception as e:
                    print(f"Error processing chapter {ch_dir.name}: {e}")

            class_summary["subjects"].append(subject_summary)

        self.catalog["classes"].append(class_summary)
        with open(RUNTIME_ROOT / "catalog.json", "w", encoding="utf-8") as f:
            json.dump(self.catalog, f, indent=2, ensure_ascii=False)

        INDEX_DIR = RUNTIME_ROOT / "search"
        INDEX_DIR.mkdir(parents=True, exist_ok=True)
        with open(INDEX_DIR / "index.json", "w", encoding="utf-8") as f:
            json.dump(self.search_index, f, indent=2, ensure_ascii=False)

    def process_chapter(self, ch_dir: Path, subj_id: str, subj_name: str) -> Dict[str, Any]:
        ch_parts = ch_dir.name.split("_", 1)
        ch_num = ch_parts[0]
        ch_title = ch_parts[1].replace("_", " ") if len(ch_parts) > 1 else ch_dir.name
        ch_uid = f"{subj_id}_{ch_num}"

        chapter = {
            "id": ch_uid, "chapter_id": ch_num, "classId": "Class 5", "subjectId": subj_name,
            "title": ch_title, "learn": [], "practice": [], "assess": [], "revise": [], "resources": [],
            "counts": {}
        }

        PILLAR_MAP = {
            "01_LEARN": "learn", "02_PRACTICE": "practice",
            "03_ASSESS": "assess", "04_REVISE": "revise",
            "05_RESOURCES": "resources"
        }

        for src_dir_name, pillar in PILLAR_MAP.items():
            src_path = ch_dir / src_dir_name
            if not src_path.exists(): continue
            items = []
            seen_normalized_hashes = set()

            json_files = sorted(src_path.rglob("*.json"))
            if pillar == "learn":
                 lesson_files = [f for f in json_files if "LESSONS.json" in f.name]
                 other_files = [f for f in json_files if "LESSONS.json" not in f.name and "full_chapter_text" not in f.name]
                 ordered_files = lesson_files + other_files
            else:
                 ordered_files = [f for f in json_files if "full_chapter_text" not in f.name]

            for jf in ordered_files:
                try:
                    with open(jf, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        raw_items = data.get("items", []) if isinstance(data, dict) else data
                        if not isinstance(raw_items, list): continue

                        for itm in raw_items:
                            if not isinstance(itm, dict): continue

                            txt = itm.get("source_text") or itm.get("text") or ""
                            section_heading = clean_text(itm.get("section") or itm.get("title") or "")

                            if section_heading:
                                 norm_h = normalize_for_dedup(section_heading)
                                 if norm_h not in seen_normalized_hashes:
                                     h_id = get_deterministic_id("c5", subj_name, ch_num, pillar, norm_h, len(items))
                                     items.append({
                                         "id": h_id, "type": "heading", "text": section_heading,
                                         "source": { "file": str(jf.relative_to(ch_dir)), "page": itm.get("source_page") or itm.get("page") },
                                         "order": len(items) + 1
                                     })
                                     seen_normalized_hashes.add(norm_h)

                            units = semantic_split(txt)
                            for u in units:
                                u_clean = clean_text(u)
                                if not u_clean or u_clean == section_heading: continue

                                norm_u = normalize_for_dedup(u_clean)
                                if norm_u in seen_normalized_hashes: continue
                                seen_normalized_hashes.add(norm_u)

                                rec_type = detect_type(u_clean, itm.get("type", "paragraph"))
                                rid = get_deterministic_id("c5", subj_name, ch_num, pillar, norm_u, len(items))

                                items.append({
                                    "id": rid, "type": rec_type, "text": u_clean,
                                    "answer": clean_text(itm.get("answer")) if itm.get("answer") else None,
                                    "source": { "file": str(jf.relative_to(ch_dir)), "page": itm.get("source_page") or itm.get("page") },
                                    "order": len(items) + 1
                                })
                except Exception: pass

            chapter[pillar] = items
            chapter["counts"][pillar] = len(items)

        return chapter

if __name__ == "__main__":
    Class5Adapter().process_all()
    print("Done.")
