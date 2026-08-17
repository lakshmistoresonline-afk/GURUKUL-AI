import os
import json
import hashlib
import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import pdfplumber

class NCERTProcessor:
    def __init__(self, config_path: str, chapter_map_path: str, question_bank_dir: Optional[str] = None):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.class_config = json.load(f)

        with open(chapter_map_path, 'r', encoding='utf-8') as f:
            self.chapter_map = json.load(f)

        self.question_bank_dir = question_bank_dir
        self.stats = {
            "pdfs_discovered": 0,
            "pdfs_processed": 0,
            "chapters_resolved": 0,
            "chapters_unresolved": 0,
            "new_packages": 0,
            "skipped_existing": 0,
            "errors": []
        }

    def calculate_hash(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def normalize_subject(self, class_id: str, folder_name: str) -> tuple:
        """Normalizes folder name to subject key and detects Part I/II."""
        config = self.class_config.get(class_id, {})
        if not config:
            return folder_name.lower(), None

        part = None
        if "Part 1" in folder_name or "Part I" in folder_name:
            part = "Part I"
        elif "Part 2" in folder_name or "Part II" in folder_name:
            part = "Part II"

        clean_name = folder_name.replace("Part 1", "").replace("Part I", "").replace("Part 2", "").replace("Part II", "").strip()

        for subj_key, subj_info in config.get("subjects", {}).items():
            if clean_name.lower() == subj_key.lower() or clean_name in subj_info.get("variants", []):
                return subj_key, part

        return clean_name.lower().replace(" ", "_"), part

    def extract_pdf_data(self, pdf_path: str) -> Dict[str, Any]:
        """Extracts text and basic metadata from PDF without AI."""
        data = {
            "text_chunks": [],
            "page_count": 0,
            "first_page_text": "",
            "chapter_num": None,
            "chapter_title": None
        }

        try:
            with pdfplumber.open(pdf_path) as pdf:
                data["page_count"] = len(pdf.pages)
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        data["text_chunks"].append({"page": i + 1, "text": text})
                        if i == 0:
                            data["first_page_text"] = text

                # Heuristic for chapter number/title on first page
                if data["first_page_text"]:
                    lines = [l.strip() for l in data["first_page_text"].split('\n') if l.strip()]
                    # Look for "Chapter X" or digit at start
                    for line in lines[:5]:
                        match = re.search(r'(?:Chapter|Lesson|Unit)\s*(\d+)', line, re.IGNORECASE)
                        if match:
                            data["chapter_num"] = int(match.group(1))
                            break

                    # Assume title is one of the first bold-looking lines
                    if len(lines) > 0:
                        data["chapter_title"] = lines[0]
        except Exception as e:
            self.stats["errors"].append(f"PDF Error {pdf_path}: {str(e)}")

        return data

    def resolve_chapter_id(self, class_id: str, subject: str, part: Optional[str], chapter_num: Optional[int], title: Optional[str]) -> str:
        """Consults registry and naming patterns to find or propose an ID."""
        # 1. Search existing map by title
        if title:
            for mapped_title, info in self.chapter_map.items():
                if mapped_title.lower() == title.lower() and info.get("class") == class_id:
                    return info["id"]

        # 2. Propose based on pattern if mapping is missing
        config = self.class_config.get(class_id, {}).get("subjects", {}).get(subject, {})
        if config and "id_pattern" in config:
            pattern = config["id_pattern"]
            part_offset = 1
            if part and "part_offsets" in config:
                part_offset = config["part_offsets"].get(part, 1)

            # Pattern like "gegp{part_offset}{chapter_num:02d}"
            try:
                # Basic substitution
                cid = pattern.replace("{chapter_num}", f"{chapter_num:02d}" if chapter_num else "xx")
                cid = cid.replace("{part_offset}", str(part_offset))
                return f"PROPOSAL_{cid}"
            except:
                pass

        return "UNRESOLVED"

    def process_directory(self, class_num: int, source_dir: str, output_dir: str, dry_run=False, update_existing=False):
        class_id = f"class_{class_num}"
        print(f"--- Processing {class_id} from {source_dir} ---")

        # Recursive scan with deduplication
        pdf_files_raw = list(Path(source_dir).rglob("*.pdf")) + list(Path(source_dir).rglob("*.PDF"))
        # Use set of absolute paths for deduplication
        seen_paths = set()
        pdf_files = []
        for p in pdf_files_raw:
            abs_p = str(p.absolute())
            if abs_p not in seen_paths:
                seen_paths.add(abs_p)
                pdf_files.append(p)

        self.stats["pdfs_discovered"] = len(pdf_files)

        for pdf_path in pdf_files:
            relative_path = pdf_path.relative_to(source_dir)
            folder_parts = relative_path.parts

            # Detect subject and part from folder structure
            subject_folder = folder_parts[0] if len(folder_parts) > 1 else "general"
            subject, part = self.normalize_subject(class_id, subject_folder)

            print(f"Processing: {pdf_path.name} | Subject: {subject} | Part: {part}")

            # Extract data
            pdf_data = self.extract_pdf_data(str(pdf_path))
            source_hash = self.calculate_hash(str(pdf_path))

            # Resolve ID
            chapter_id = self.resolve_chapter_id(
                class_id, subject, part, pdf_data["chapter_num"], pdf_path.stem
            )

            if "PROPOSAL" in chapter_id or chapter_id == "UNRESOLVED":
                self.stats["chapters_unresolved"] += 1
            else:
                self.stats["chapters_resolved"] += 1

            # Build package
            package = self.assemble_package(
                class_id, subject, part, chapter_id, pdf_path.name, source_hash, pdf_data
            )

            # Determine output path
            target_dir = os.path.join(output_dir, class_id, subject, chapter_id)
            package_path = os.path.join(target_dir, "package.json")

            if os.path.exists(package_path) and not update_existing:
                self.stats["skipped_existing"] += 1
                if dry_run: print(f"  [DRY-RUN] Skip existing: {package_path}")
                continue

            if dry_run:
                print(f"  [DRY-RUN] Would create: {package_path}")
                self.stats["pdfs_processed"] += 1
                continue

            # Physical Write
            os.makedirs(target_dir, exist_ok=True)
            with open(package_path, 'w', encoding='utf-8') as f:
                json.dump(package, f, indent=2, ensure_ascii=False)

            self.stats["pdfs_processed"] += 1
            self.stats["new_packages"] += 1
            print(f"  [SUCCESS] Generated package for {chapter_id}")

    def assemble_package(self, class_id, subject, part, chapter_id, filename, source_hash, pdf_data):
        now = datetime.utcnow().isoformat() + "Z"

        # Merge Question Bank if available
        questions = []
        if self.question_bank_dir:
            qb_path = os.path.join(self.question_bank_dir, class_id, subject, f"{chapter_id.replace('PROPOSAL_', '')}.json")
            if os.path.exists(qb_path):
                try:
                    with open(qb_path, 'r', encoding='utf-8') as f:
                        qb_data = json.load(f)
                        questions = qb_data.get("questions", [])
                except: pass

        return {
            "metadata": {
                "job_id": f"pipeline_{chapter_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "class_name": class_id,
                "subject": subject,
                "chapter_id": chapter_id,
                "chapter_name": pdf_data["chapter_title"] or filename,
                "part": part,
                "source_pdf": filename,
                "source_hash": source_hash,
                "processed_at": now,
                "is_final_content": False
            },
            "content": {
                "topic": pdf_data["chapter_title"] or chapter_id,
                "introduction": "pending_enrichment",
                "summary": "pending_enrichment",
                "teacher_explanation": "pending_enrichment",
                "story_explanation": "pending_enrichment",
                "quiz": questions[:8],
                "flashcards": []
            },
            "original_data": {
                "schemaVersion": "3.0",
                "curriculum": {
                    "board": "NCERT",
                    "class": int(class_id.split("_")[-1]),
                    "subject": subject,
                    "chapterTitle": pdf_data["chapter_title"],
                    "chapterId": chapter_id
                },
                "source": {
                    "sourceFile": filename,
                    "pageCount": pdf_data["page_count"]
                },
                "sourceContent": {
                    "pageChunks": pdf_data["text_chunks"]
                },
                "aiEnrichment": {
                    "status": "pending_enrichment"
                },
                "assessment": {
                    "expandedQuestionBank": questions
                }
            }
        }

    def generate_report(self, output_dir: str):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        report_path_json = os.path.join(output_dir, "NCERT_PROCESSING_REPORT.json")
        report_path_md = os.path.join(output_dir, "NCERT_PROCESSING_REPORT.md")

        with open(report_path_json, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2)

        with open(report_path_md, 'w', encoding='utf-8') as f:
            f.write("# NCERT Content Processing Report\n\n")
            f.write(f"Generated at: {datetime.now().isoformat()}\n\n")
            f.write(f"* PDFs Discovered: {self.stats['pdfs_discovered']}\n")
            f.write(f"* PDFs Processed: {self.stats['pdfs_processed']}\n")
            f.write(f"* Chapters Resolved: {self.stats['chapters_resolved']}\n")
            f.write(f"* Chapters Unresolved/Proposed: {self.stats['chapters_unresolved']}\n")
            f.write(f"* New Packages: {self.stats['new_packages']}\n")
            f.write(f"* Skipped (Existing): {self.stats['skipped_existing']}\n\n")

            if self.stats["errors"]:
                f.write("## Errors\n")
                for err in self.stats["errors"]:
                    f.write(f"* {err}\n")

def main():
    parser = argparse.ArgumentParser(description="Gurukul AI NCERT Content Processor (Deterministic)")
    parser.add_argument("--class", type=int, required=True, dest="class_num", help="Class level (e.g. 7, 8)")
    parser.add_argument("--source-dir", required=True, help="Path to NCERT source PDFs")
    parser.add_argument("--output-dir", required=True, help="Path for staging output")
    parser.add_argument("--question-bank-dir", help="Optional path to Question Bank JSONs")
    parser.add_argument("--dry-run", action="store_true", help="Report only, no writes")
    parser.add_argument("--update-existing", action="store_true", help="Overwrite existing packages")
    parser.add_argument("--verbose", action="store_true", help="Detailed logging")

    args = parser.parse_args()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(project_root, "config", "ncert_classes.json")
    chapter_map_path = os.path.join(project_root, "backend", "storage", "chapter_title_map.json")

    processor = NCERTProcessor(config_path, chapter_map_path, args.question_bank_dir)
    processor.process_directory(args.class_num, args.source_dir, args.output_dir, args.dry_run, args.update_existing)
    processor.generate_report(args.output_dir)

if __name__ == "__main__":
    main()
