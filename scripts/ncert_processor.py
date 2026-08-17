import os
import json
import hashlib
import argparse
import sys
import shutil
from datetime import datetime
from pathlib import Path

# Add backend/src to path to reuse utilities if needed,
# but we aim for a standalone deterministic script for the automation task.
# sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def extract_text_from_pdf(file_path):
    # Using pypdf as it's in requirements.txt
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        text_chunks = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                text_chunks.append({"page": i + 1, "text": text})
        return text_chunks
    except ImportError:
        print("Error: pypdf not found. Please install it with 'pip install pypdf'")
        return []
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return []

def get_chapter_id_from_map(title_map, chapter_title):
    # Try exact match first
    chapter_title_lower = chapter_title.lower()
    if chapter_title_lower in title_map:
        return title_map[chapter_title_lower]["id"]

    # Try fuzzy match (title is inside)
    for title, info in title_map.items():
        if title in chapter_title_lower or chapter_title_lower in title:
            return info["id"]

    return None

def process_chapter(class_name, subject, pdf_path, output_root, title_map, question_bank_root, dry_run=False, update_existing=False):
    file_name = os.path.basename(pdf_path)
    chapter_id_from_file = os.path.splitext(file_name)[0] # e.g. eemm101

    # Try to find human readable name from title_map
    chapter_name = "Unknown Chapter"
    actual_chapter_id = chapter_id_from_file

    for title, info in title_map.items():
        if info["id"] == chapter_id_from_file:
            chapter_name = title.title()
            break

    # Determine paths
    target_dir = os.path.join(output_root, class_name, subject, actual_chapter_id)
    package_path = os.path.join(target_dir, "package.json")

    if os.path.exists(package_path) and not update_existing:
        print(f"  [SKIP] Package already exists at {package_path}. Use --update-existing to overwrite.")
        return False

    print(f"  [PROCESS] {file_name} -> {actual_chapter_id} ({chapter_name})")

    if dry_run:
        print(f"    (Dry-run) Would create package at {package_path}")
        return True

    # 1. SHA256
    file_hash = calculate_sha256(pdf_path)

    # 2. Text Extraction
    text_chunks = extract_text_from_pdf(pdf_path)
    full_text = "\n\n".join([c["text"] for c in text_chunks])

    # 3. Question Bank Matching
    # Question Bank files are usually named [slug].json or [chapter_id].json
    # Based on audit, class 5 math has 'we-the-travellers-i.json' which is slugified title.
    # Let's try matching by ID and Slug.
    slug = chapter_name.lower().replace(" ", "-").replace("—", "-").replace("--", "-").strip("-")
    qb_file_candidates = [
        os.path.join(question_bank_root, class_name, subject, f"{actual_chapter_id}.json"),
        os.path.join(question_bank_root, class_name, subject, f"{slug}.json")
    ]

    qb_data = None
    for qb_path in qb_file_candidates:
        if os.path.exists(qb_path):
            with open(qb_path, "r", encoding="utf-8") as f:
                qb_data = json.load(f)
                print(f"    [INFO] Matched Question Bank: {os.path.basename(qb_path)}")
                break

    # 4. Assemble package.json
    package = {
        "metadata": {
            "job_id": f"auto_{actual_chapter_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "class_name": class_name,
            "subject": subject,
            "chapter_id": actual_chapter_id,
            "chapter_name": chapter_name,
            "completed_at": datetime.utcnow().isoformat() + "Z",
            "is_final_content": True,
            "source_file_hash": file_hash
        },
        "content": {
            "topic": chapter_name,
            "introduction": f"This chapter is organised around “{chapter_name}”.",
            "summary": f"Summary for {chapter_name} derived from NCERT source.",
            "teacher_explanation": full_text[:1000] + "...", # Placeholder/Truncated
            "story_explanation": "Refer to the original textbook story.",
            "concepts": [], # Deterministic extraction would require more logic, keeping empty for now
            "quiz": [],
            "flashcards": []
        },
        "original_data": {
            "schemaVersion": "3.0",
            "curriculum": {
                "board": "NCERT",
                "class": int(class_name.split("_")[-1]),
                "subject": subject,
                "chapterTitle": chapter_name,
                "chapterId": actual_chapter_id
            },
            "source": {
                "sourceFile": file_name,
                "sourceType": "NCERT PDF",
                "pageCount": len(text_chunks)
            },
            "sourceContent": {
                "pageChunks": text_chunks
            }
        }
    }

    # Merge questions if available
    if qb_data and "questions" in qb_data:
        package["content"]["quiz"] = qb_data["questions"][:8] # Match existing 8-question contract
        package["original_data"]["assessment"] = {
            "expandedQuestionBank": qb_data["questions"]
        }

    # 5. Save
    os.makedirs(target_dir, exist_ok=True)
    with open(package_path, "w", encoding="utf-8") as f:
        json.dump(package, f, indent=2, ensure_ascii=False)

    print(f"    [SUCCESS] Created package at {package_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Deterministic NCERT PDF Processor (No-AI)")
    parser.add_argument("--classes", help="Comma-separated class levels (e.g. 5,6)", default="5,6")
    parser.add_argument("--chapter", help="Specific chapter ID to process")
    parser.add_argument("--update-existing", action="store_true", help="Overwrite existing packages")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--verbose", action="store_true", help="Show detailed logs")

    args = parser.parse_args()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_root = os.path.join(project_root, "backend", "storage", "output")
    ncert_source_root = os.path.join(project_root, "archive", "historical_scripts", "maintenance_archive", "datasets", "ncert_source")
    title_map_path = os.path.join(project_root, "backend", "storage", "chapter_title_map.json")
    question_bank_root = os.path.join(project_root, "Question Bank")

    if not os.path.exists(title_map_path):
        print(f"Error: Chapter title map not found at {title_map_path}")
        return

    with open(title_map_path, "r", encoding="utf-8") as f:
        title_map = json.load(f)

    classes_to_process = [f"class_{c.strip()}" for c in args.classes.split(",")]

    print(f"Starting NCERT Processing for: {', '.join(classes_to_process)}")
    if args.dry_run: print("!!! DRY RUN MODE - No changes will be saved !!!")

    stats = {"processed": 0, "skipped": 0, "errors": 0}

    for class_name in classes_to_process:
        class_path = os.path.join(ncert_source_root, class_name)
        if not os.path.exists(class_path):
            print(f"Warning: Source path not found for {class_name}")
            continue

        for subject in os.listdir(class_path):
            subj_path = os.path.join(class_path, subject)
            if not os.path.isdir(subj_path): continue

            print(f"\nProcessing {class_name} - {subject}")

            for file in os.listdir(subj_path):
                if not file.lower().endswith(".pdf"): continue

                chapter_id = os.path.splitext(file)[0]
                if args.chapter and args.chapter != chapter_id:
                    continue

                try:
                    success = process_chapter(
                        class_name, subject, os.path.join(subj_path, file),
                        output_root, title_map, question_bank_root,
                        dry_run=args.dry_run, update_existing=args.update_existing
                    )
                    if success: stats["processed"] += 1
                    else: stats["skipped"] += 1
                except Exception as e:
                    print(f"  [ERROR] Failed to process {file}: {e}")
                    stats["errors"] += 1

    print("\n" + "="*40)
    print("NCERT PROCESSING REPORT")
    print("="*40)
    print(f"Total Processed: {stats['processed']}")
    print(f"Total Skipped:   {stats['skipped']}")
    print(f"Total Errors:    {stats['errors']}")
    print("="*40)

if __name__ == "__main__":
    main()
