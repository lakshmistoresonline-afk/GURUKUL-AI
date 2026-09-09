from pathlib import Path
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime

PROJECT_ROOT = Path(r"D:\GURUKUL-AI")
ENGLISH_ROOT = PROJECT_ROOT / "Contents" / "Class 5" / "01_ENGLISH_COMPLETE" / "01_ENGLISH"
ADAPTER = PROJECT_ROOT / "backend" / "scripts" / "canonical_adapter_class5.py"

CHAPTER_RE = re.compile(r"^(10[1-9]|110)_")

GENERIC_MCQ_PHRASES = [
    "which source section should be used",
    "an unrelated chapter",
    "an external invented story",
]

GENERIC_SHORT_PHRASES = [
    "in your own words, explain one important idea from this chapter",
]


def load_json(path):
    if not path.exists():
        return None

    raw = path.read_bytes()

    for encoding in ("utf-8-sig", "utf-16", "utf-16-le", "utf-16-be"):
        try:
            return json.loads(raw.decode(encoding))
        except Exception:
            pass

    return None


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def text_of(item):
    if not isinstance(item, dict):
        return ""

    for key in (
        "question_or_prompt",
        "question",
        "prompt",
        "text",
        "content",
        "body",
    ):
        value = item.get(key)
        if isinstance(value, str):
            return value.strip()

    return ""


def source_ref_of(item, fallback):
    if not isinstance(item, dict):
        return fallback

    return (
        item.get("source_ref")
        or item.get("source")
        or fallback
    )


def is_generic_generated(item):
    text = text_of(item).lower()

    if not text:
        return True

    for phrase in GENERIC_MCQ_PHRASES:
        if phrase in text:
            return True

    for phrase in GENERIC_SHORT_PHRASES:
        if phrase in text:
            return True

    return False


def is_complete_question(text):
    if not text:
        return False

    text = re.sub(r"\s+", " ", text).strip()

    # Reject obvious OCR fragments.
    if len(text) < 15:
        return False

    if text.endswith("?"):
        return True

    # Some extracted questions lose the final punctuation.
    if re.match(r"^\d+[\.\)]\s+", text):
        words = text.split()
        if len(words) >= 7:
            return True

    return False


def explicit_mcq(item):
    if not isinstance(item, dict):
        return None

    if is_generic_generated(item):
        return None

    options = (
        item.get("options")
        or item.get("choices")
        or item.get("answers")
    )

    if not isinstance(options, list) or len(options) < 2:
        return None

    question = text_of(item)

    if not question:
        return None

    result = {
        "question": question,
        "options": options,
        "source_ref": source_ref_of(item, ""),
        "source_page": item.get("source_page") or item.get("page"),
        "status": "SOURCE_DERIVED",
        "assessment_origin": "EXPLICIT_SOURCE_MCQ",
    }

    if item.get("answer") is not None:
        result["answer"] = item["answer"]

    return result


def collect_explicit_mcqs(chapter_dir):
    candidates = []

    # Existing MCQ file.
    mcq_file = (
        chapter_dir
        / "03_ASSESS"
        / "02_MCQ"
        / "MCQ.json"
    )

    data = load_json(mcq_file)

    if isinstance(data, dict):
        items = data.get("items", [])
        if isinstance(items, list):
            candidates.extend(items)

    # Also inspect every assessment JSON for explicit option sets.
    assess_dir = chapter_dir / "03_ASSESS"

    if assess_dir.exists():
        for path in assess_dir.rglob("*.json"):
            data = load_json(path)

            if not isinstance(data, dict):
                continue

            items = data.get("items", [])

            if not isinstance(items, list):
                continue

            candidates.extend(items)

    output = []
    seen = set()

    for item in candidates:
        mcq = explicit_mcq(item)

        if not mcq:
            continue

        key = json.dumps(
            [mcq["question"], mcq["options"]],
            ensure_ascii=False,
            sort_keys=True,
        )

        if key in seen:
            continue

        seen.add(key)
        output.append(mcq)

    return output


def collect_source_questions(chapter_dir):
    path = (
        chapter_dir
        / "02_PRACTICE"
        / "02_QUESTIONS"
        / "QUESTIONS.json"
    )

    data = load_json(path)

    if not isinstance(data, dict):
        return []

    items = data.get("items", [])

    if not isinstance(items, list):
        return []

    output = []
    seen = set()

    for item in items:
        text = text_of(item)

        if not is_complete_question(text):
            continue

        normalized = re.sub(r"\s+", " ", text).lower()

        if normalized in seen:
            continue

        seen.add(normalized)

        output.append({
            "question": text,
            "source_ref": source_ref_of(
                item,
                f"{chapter_dir.name}/02_PRACTICE/02_QUESTIONS/QUESTIONS.json"
            ),
            "source_page": item.get("source_page") or item.get("page"),
            "status": "SOURCE_DERIVED",
            "assessment_origin": "TEXTBOOK_QUESTION_REUSE",
        })

    return output


def build_chapter(chapter_dir):
    chapter_id = chapter_dir.name.split("_", 1)[0]

    mcqs = collect_explicit_mcqs(chapter_dir)
    source_questions = collect_source_questions(chapter_dir)

    # Do not duplicate textbook questions already represented as
    # explicit textbook assessments.
    textbook_assessments_file = (
        chapter_dir
        / "03_ASSESS"
        / "01_TEXTBOOK_ASSESSMENTS"
        / "TEXTBOOK_ASSESSMENTS.json"
    )

    textbook_data = load_json(textbook_assessments_file)

    existing_questions = set()

    if isinstance(textbook_data, dict):
        for item in textbook_data.get("items", []):
            text = text_of(item)

            if text:
                existing_questions.add(
                    re.sub(r"\s+", " ", text).lower()
                )

    short_answers = []

    for item in source_questions:
        key = re.sub(
            r"\s+",
            " ",
            item["question"]
        ).lower()

        if key in existing_questions:
            continue

        short_answers.append({
            "question": item["question"],
            "answer_guidance": (
                "Answer using evidence from the source chapter. "
                "Do not introduce information not supported by the textbook."
            ),
            "source_ref": item["source_ref"],
            "source_page": item["source_page"],
            "status": "SOURCE_DERIVED",
            "assessment_origin": "TEXTBOOK_QUESTION_REUSE",
        })

    gaps = []

    if not mcqs:
        gaps.append({
            "category": "MCQ",
            "status": "GAP_RECORDED",
            "reason": (
                "No explicit source-derived multiple-choice question "
                "with answer options was found in the chapter package."
            ),
        })

    if not short_answers:
        gaps.append({
            "category": "SHORT_ANSWER",
            "status": "GAP_RECORDED",
            "reason": (
                "No additional complete source-derived textbook question "
                "was available for assessment reuse."
            ),
        })

    # ------------------------------------------------------------
    # SOURCE-GROUNDED MCQ
    # ------------------------------------------------------------

    if mcqs:
        mcq_dir = (
            chapter_dir
            / "03_ASSESS"
            / "04_SOURCE_GROUNDED_MCQ"
        )

        save_json(
            mcq_dir / "MCQ.json",
            {
                "chapter_id": chapter_id,
                "status": "SOURCE_DERIVED",
                "items": mcqs,
            }
        )

    # ------------------------------------------------------------
    # SOURCE-GROUNDED SHORT ANSWER
    # ------------------------------------------------------------

    if short_answers:
        short_dir = (
            chapter_dir
            / "03_ASSESS"
            / "05_SOURCE_GROUNDED_SHORT_ANSWER"
        )

        save_json(
            short_dir / "SHORT_ANSWER.json",
            {
                "chapter_id": chapter_id,
                "status": "SOURCE_DERIVED",
                "items": short_answers,
            }
        )

    # ------------------------------------------------------------
    # ASSESSMENT GAP RECORD
    # ------------------------------------------------------------

    gap_dir = (
        chapter_dir
        / "99_INTERNAL_TRACEABILITY"
        / "ASSESSMENT_GAPS"
    )

    save_json(
        gap_dir / "ASSESSMENT_GAPS.json",
        {
            "chapter_id": chapter_id,
            "generated_at": datetime.now().isoformat(),
            "policy": "SOURCE_GROUNDED_ONLY",
            "gaps": gaps,
        }
    )

    return {
        "chapter": chapter_id,
        "mcq": len(mcqs),
        "short_answer": len(short_answers),
        "gaps": len(gaps),
    }


def main():
    print("")
    print("=" * 72)
    print("CLASS 5 ENGLISH — SOURCE-GROUNDED ASSESSMENT ENRICHMENT")
    print("=" * 72)
    print("")

    if not ENGLISH_ROOT.exists():
        print("ERROR: English content root not found:")
        print(ENGLISH_ROOT)
        sys.exit(1)

    chapters = sorted(
        [
            p for p in ENGLISH_ROOT.iterdir()
            if p.is_dir() and CHAPTER_RE.match(p.name)
        ],
        key=lambda p: p.name
    )

    if len(chapters) != 10:
        print(
            f"ERROR: Expected 10 English chapters, found {len(chapters)}"
        )
        sys.exit(1)

    results = []

    for chapter in chapters:
        result = build_chapter(chapter)
        results.append(result)

        print(
            f"{result['chapter']}  "
            f"MCQ={result['mcq']}  "
            f"SHORT_ANSWER={result['short_answer']}  "
            f"GAPS={result['gaps']}"
        )

    manifest = {
        "status": "SOURCE_GROUNDED_ASSESSMENT_ENRICHMENT",
        "subject": "English",
        "class": 5,
        "chapters": results,
        "rules": [
            "No invented MCQs",
            "No replacement of original source files",
            "Explicit source MCQs preserved",
            "Complete textbook questions reused as source-derived assessment prompts",
            "Missing source categories recorded as GAP_RECORDED",
        ],
    }

    manifest_path = (
        PROJECT_ROOT
        / "runtime-data"
        / "CLASS5_ENGLISH_ASSESSMENT_ENRICHMENT_MANIFEST.json"
    )

    save_json(manifest_path, manifest)

    print("")
    print("Assessment source files created.")
    print(f"Manifest: {manifest_path}")
    print("")

    # Rebuild canonical runtime immediately.
    if not ADAPTER.exists():
        print("ERROR: canonical adapter not found:")
        print(ADAPTER)
        sys.exit(1)

    print("Rebuilding Class 5 canonical runtime...")
    print("")

    completed = subprocess.run(
        [sys.executable, str(ADAPTER)],
        cwd=str(PROJECT_ROOT),
        check=False,
    )

    if completed.returncode != 0:
        print("")
        print("ERROR: canonical adapter failed.")
        sys.exit(completed.returncode)

    print("")
    print("=" * 72)
    print("CLASS 5 ENGLISH ASSESSMENT ENRICHMENT COMPLETE")
    print("=" * 72)
    print("")
    print("The original source files were not overwritten.")
    print("The canonical runtime has been rebuilt.")
    print("")


if __name__ == "__main__":
    main()