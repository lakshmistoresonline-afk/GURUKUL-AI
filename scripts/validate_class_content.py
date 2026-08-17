import os
import json
import argparse
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Set

class ClassContentValidator:
    def __init__(self, class_num: int, content_dir: str, config_path: str, verbose: bool = False):
        self.class_num = class_num
        self.class_id = f"class_{class_num}"
        self.content_dir = content_dir
        self.verbose = verbose

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f).get(self.class_id, {})

        self.report = {
            "class": self.class_id,
            "contentDirectory": content_dir,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "totalPackages": 0,
                "validPackages": 0,
                "invalidPackages": 0,
                "totalChapters": 0,
                "questionCount": 0,
                "conceptCount": 0,
                "masteryChapterCount": 0,
                "youtubeChapterCount": 0,
                "externalMultimediaChapterCount": 0
            },
            "checks": {},
            "errors": [],
            "warnings": [],
            "reviewRequired": [],
            "readyForProduction": False,
            "structuralReady": False,
            "pedagogicallyReviewed": False
        }

        self.discovered_chapter_ids = set()
        self.package_data = {} # chapter_id -> data
        self.master_data = {}
        self.multimedia_data = {}

    def log(self, message: str):
        if self.verbose:
            print(f"[INFO] {message}")

    def add_error(self, message: str):
        self.report["errors"].append(message)
        if self.verbose:
            print(f"[ERROR] {message}")

    def add_warning(self, message: str):
        self.report["warnings"].append(message)
        if self.verbose:
            print(f"[WARNING] {message}")

    def add_review(self, message: str):
        self.report["reviewRequired"].append(message)
        if self.verbose:
            print(f"[REVIEW] {message}")

    def normalize_subject(self, subject: str) -> str:
        """Normalizes subject names (e.g. Mathematics Part 1 -> Mathematics)."""
        s = subject.strip().replace("_", " ")
        s = re.sub(r'\s+Part\s+[IVX12]+$', '', s, flags=re.IGNORECASE)
        if s.lower() == "maths": return "Mathematics"
        return s

    def validate_chapter_packages(self):
        self.log("Validating Chapter Packages...")
        pkg_dir = None
        for d in os.listdir(self.content_dir):
            if d.startswith("01_") and "_Chapter_Packages" in d:
                pkg_dir = os.path.join(self.content_dir, d)
                break

        if not pkg_dir:
            self.add_error("Chapter packages directory (01_...) not found.")
            return

        package_files = []
        for root, _, files in os.walk(pkg_dir):
            for f in files:
                if f == "package.json":
                    package_files.append(os.path.join(root, f))

        self.report["summary"]["totalPackages"] = len(package_files)

        for pkg_path in package_files:
            self.validate_single_package(pkg_path)

        # Check chapter counts
        expected_count = self.config.get("expected_chapters")
        discovered_count = len(self.discovered_chapter_ids)
        self.report["summary"]["totalChapters"] = discovered_count

        if expected_count and discovered_count != expected_count:
            self.add_error(f"Chapter count mismatch. Expected {expected_count}, found {discovered_count}.")

        # Subject distribution check
        subject_counts = {}
        for cid, data in self.package_data.items():
            raw_subj = data.get("metadata", {}).get("subject", "Unknown")
            norm_subj = self.normalize_subject(raw_subj)

            # Match against config subjects
            matched = False
            for expected_subj in self.config.get("expected_subjects", []):
                if norm_subj.lower() == expected_subj.lower():
                    subject_counts[expected_subj] = subject_counts.get(expected_subj, 0) + 1
                    matched = True
                    break
            if not matched:
                subject_counts[norm_subj] = subject_counts.get(norm_subj, 0) + 1

        expected_subject_counts = self.config.get("subject_chapter_counts", {})
        for subj, count in expected_subject_counts.items():
            if subject_counts.get(subj, 0) != count:
                self.add_error(f"Subject '{subj}' count mismatch. Expected {count}, found {subject_counts.get(subj, 0)}.")

    def validate_single_package(self, path: str):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.add_error(f"Invalid JSON in {path}: {str(e)}")
            self.report["summary"]["invalidPackages"] += 1
            return

        cid = data.get("metadata", {}).get("chapter_id")
        if not cid:
            self.add_error(f"Missing chapter_id in {path}")
            self.report["summary"]["invalidPackages"] += 1
            return

        if cid in self.discovered_chapter_ids:
            self.add_error(f"Duplicate chapter_id found: {cid} at {path}")
        self.discovered_chapter_ids.add(cid)
        self.package_data[cid] = data

        # Directory name match check
        dir_name = os.path.basename(os.path.dirname(path))
        if dir_name != cid:
            self.add_warning(f"Directory name '{dir_name}' does not match chapter_id '{cid}'")

        # Required fields check
        required_top = ["metadata", "content", "original_data"]
        for field in required_top:
            if field not in data:
                self.add_error(f"[{cid}] Missing top-level field: {field}")

        meta = data.get("metadata", {})
        # Flexible hash check
        has_hash = "source_hash" in meta or "source_sha256" in meta or "source_sha256" in data.get("original_data", {}).get("source", {})

        required_meta = ["class_name", "subject", "chapter_id", "chapter_name"]
        for field in required_meta:
            if field not in meta or not meta[field]:
                self.add_error(f"[{cid}] Missing metadata field: {field}")

        if not has_hash:
             self.add_error(f"[{cid}] Missing source hash")

        if meta.get("class_name") != self.class_id:
            self.add_error(f"[{cid}] Class mismatch. Package says {meta.get('class_name')}, expected {self.class_id}")

        content = data.get("content", {})
        required_content = ["topic", "introduction", "summary", "teacher_explanation", "story_explanation", "quiz", "flashcards"]
        for field in required_content:
            if field not in content:
                self.add_error(f"[{cid}] Missing content field: {field}")

        # Deep data checks
        orig = data.get("original_data", {})
        if "aiEnrichment" not in orig: self.add_error(f"[{cid}] Missing original_data.aiEnrichment")
        if "assessment" not in orig: self.add_error(f"[{cid}] Missing original_data.assessment")

        # Check quiz structure
        quiz = content.get("quiz", [])
        if not isinstance(quiz, list):
            self.add_error(f"[{cid}] Content.quiz must be an array")
        else:
            for i, q in enumerate(quiz):
                if "question" not in q: self.add_error(f"[{cid}] Quiz item {i} missing 'question'")

        self.report["summary"]["validPackages"] += 1

    def validate_master_data(self):
        self.log("Validating Master Data...")
        master_dir = None
        for d in os.listdir(self.content_dir):
            if d.startswith("02_") and "_Master_Data" in d:
                master_dir = os.path.join(self.content_dir, d)
                break

        if not master_dir:
            self.add_error("Master data directory (02_...) not found.")
            return

        files = {
            "registry": [f"{self.class_id}_chapter_registry.json", f"class{self.class_num}_chapter_registry.json"],
            "question_bank": [f"{self.class_id}_question_bank_master.json", f"class{self.class_num}_question_bank_master.json"],
            "concepts": [f"{self.class_id}_concepts_master.json", f"class{self.class_num}_concepts_master.json"],
            "mastery": [f"{self.class_id}_mastery_data.json", f"class{self.class_num}_mastery_data.json"]
        }

        for key, candidates in files.items():
            path = None
            for c in candidates:
                p = os.path.join(master_dir, c)
                if os.path.exists(p):
                    path = p
                    break

            if not path:
                self.add_error(f"Master file missing (tried {candidates})")
                continue
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.master_data[key] = json.load(f)
            except Exception as e:
                self.add_error(f"Invalid JSON in master file: {str(e)}")

        # 1. Registry vs Packages
        reg_data = self.master_data.get("registry")
        reg_ids = set()
        if isinstance(reg_data, dict):
             reg_chapters = reg_data.get("chapters", [])
        elif isinstance(reg_data, list):
             reg_chapters = reg_data
        else:
             reg_chapters = []

        for entry in reg_chapters:
            cid = entry.get("id") or entry.get("chapterId")
            if cid: reg_ids.add(cid)

        missing_in_reg = self.discovered_chapter_ids - reg_ids
        for mid in missing_in_reg:
            self.add_error(f"Chapter {mid} exists in packages but missing from registry.")

        extra_in_reg = reg_ids - self.discovered_chapter_ids
        for eid in extra_in_reg:
            self.add_error(f"Chapter {eid} defined in registry but package.json not found.")

        # 2. Question Bank
        qb = self.master_data.get("question_bank", {})
        if qb:
            q_list = qb.get("questions", [])
            self.report["summary"]["questionCount"] = len(q_list)
            q_ids = set()
            for q in q_list:
                qid = q.get("id")
                if not qid: self.add_error("Question missing ID in master bank")
                elif qid in q_ids: self.add_error(f"Duplicate question ID: {qid}")
                q_ids.add(qid)

        # 3. Concepts
        concepts_data = self.master_data.get("concepts", {})
        if isinstance(concepts_data, dict):
            concepts_chapters = concepts_data.get("chapters", [])
            chapters_with_concepts = set()
            total_concepts = 0
            if concepts_chapters:
                for c_entry in concepts_chapters:
                    cid = c_entry.get("chapterId") or c_entry.get("chapter")
                    if cid: chapters_with_concepts.add(cid)
                    total_concepts += len(c_entry.get("concepts", []))

            self.report["summary"]["conceptCount"] = total_concepts
            missing_concepts = self.discovered_chapter_ids - chapters_with_concepts
            if missing_concepts:
                self.add_review(f"{len(missing_concepts)} chapters missing concepts in master list.")

        # 4. Mastery
        mastery_data = self.master_data.get("mastery", {})
        if mastery_data:
            m_chapters_raw = mastery_data.get("chapters", [])
            m_chapter_ids = set()

            # Handle list or dict
            if isinstance(m_chapters_raw, dict):
                for mc_id, mc_info in m_chapters_raw.items():
                    m_chapter_ids.add(mc_id)
            elif isinstance(m_chapters_raw, list):
                for mc in m_chapters_raw:
                    mc_id = mc.get("chapterId") or mc.get("id")
                    if mc_id: m_chapter_ids.add(mc_id)

            self.report["summary"]["masteryChapterCount"] = len(m_chapter_ids)
            missing_mastery = self.discovered_chapter_ids - m_chapter_ids
            if missing_mastery:
                self.add_review(f"{len(missing_mastery)} chapters missing from mastery data.")

    def validate_multimedia(self):
        self.log("Validating Multimedia Data...")
        multi_dir = None
        for d in os.listdir(self.content_dir):
            if d.startswith("03_") and "_Multimedia_Data" in d:
                multi_dir = os.path.join(self.content_dir, d)
                break

        if not multi_dir:
            self.add_error("Multimedia directory (03_...) not found.")
            return

        yt_path = os.path.join(multi_dir, f"{self.class_id}_youtube_video_resources_mapped.json")
        ext_path = os.path.join(multi_dir, f"{self.class_id}_external_multimedia_catalog.json")

        # Fallback to classN naming
        if not os.path.exists(yt_path): yt_path = os.path.join(multi_dir, f"class{self.class_num}_youtube_video_resources_mapped.json")
        if not os.path.exists(ext_path): ext_path = os.path.join(multi_dir, f"class{self.class_num}_external_multimedia_catalog.json")

        # YouTube
        if os.path.exists(yt_path):
            try:
                with open(yt_path, 'r', encoding='utf-8') as f:
                    yt = json.load(f)
                    yt_chapters = yt.get("chapters", {}) if isinstance(yt, dict) else {}
                    self.report["summary"]["youtubeChapterCount"] = len(yt_chapters)
            except Exception as e:
                self.add_error(f"Invalid YouTube JSON: {str(e)}")

        # External
        if os.path.exists(ext_path):
            try:
                with open(ext_path, 'r', encoding='utf-8') as f:
                    ext = json.load(f)
                    items = []
                    if isinstance(ext, list): items = ext
                    elif isinstance(ext, dict): items = ext.get("chapters", ext.get("chapter_resources", []))

                    ext_chapters = set()
                    for item in items:
                        cid = item.get("chapter_id") or item.get("chapterId")
                        if cid: ext_chapters.add(cid)
                    self.report["summary"]["externalMultimediaChapterCount"] = len(ext_chapters)
            except Exception as e:
                self.add_error(f"Invalid External Multimedia JSON: {str(e)}")

    def check_contamination(self):
        self.log("Performing Contamination Check...")
        found = False
        for cid, data in self.package_data.items():
            content_str = json.dumps(data)
            # Match class_5/6 but avoid matching if it's the target class
            for c in [5, 6]:
                if f"class_{c}" in content_str or f"class{c}" in content_str:
                    self.add_warning(f"Potential contamination in package {cid} (mentions class_{c})")
                    found = True

        self.report["checks"]["contamination"] = "CONTAMINATION_FOUND" if found else "NO_CONTAMINATION_FOUND"

    def check_production_safety(self):
        self.log("Checking Production Safety...")
        output_dir = os.path.abspath(os.path.join(self.content_dir, "..", "backend", "storage", "output"))
        staging_dir = os.path.abspath(self.content_dir)
        if output_dir in staging_dir:
             self.add_error("CRITICAL: Staging directory is inside production output!")
             self.report["checks"]["productionSafety"] = "FAIL"
        else:
             self.report["checks"]["productionSafety"] = "PASS"

    def finalize_readiness(self):
        errors = self.report["errors"]
        self.report["structuralReady"] = len(errors) == 0
        self.report["pedagogicallyReviewed"] = len(self.report["reviewRequired"]) == 0
        self.report["readyForProduction"] = self.report["structuralReady"]

    def generate_report(self):
        self.finalize_readiness()
        json_path = os.path.join(self.content_dir, f"{self.class_id.upper()}_FINAL_VALIDATION_REPORT.json")
        md_path = os.path.join(self.content_dir, f"{self.class_id.upper()}_FINAL_VALIDATION_REPORT.md")

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2)

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# Gurukul AI — {self.class_id.upper()} Final Validation Report\n\n")
            f.write(f"* Generated: {self.report['timestamp']}\n")
            f.write(f"* Content Directory: {self.content_dir}\n")
            f.write(f"* Structural Ready: {'✅ YES' if self.report['structuralReady'] else '❌ NO'}\n")
            f.write(f"* Production Ready: {'🚀 YES' if self.report['readyForProduction'] else '⚠️ NO'}\n\n")

            f.write("## Summary\n")
            for k, v in self.report["summary"].items():
                f.write(f"* {k}: {v}\n")

            if self.report["errors"]:
                f.write("\n## ❌ Errors\n")
                for err in self.report["errors"]:
                    f.write(f"* {err}\n")

            if self.report["warnings"]:
                f.write("\n## ⚠️ Warnings\n")
                for warn in self.report["warnings"]:
                    f.write(f"* {warn}\n")

            if self.report["reviewRequired"]:
                f.write("\n## 🔍 Review Required\n")
                for item in self.report["reviewRequired"]:
                    f.write(f"* {item}\n")

def main():
    parser = argparse.ArgumentParser(description="Gurukul AI Reusable Content Validator")
    parser.add_argument("--class", type=int, required=True, dest="class_num", help="Class level")
    parser.add_argument("--content-dir", required=True, help="Path to staging content directory")
    parser.add_argument("--verbose", action="store_true", help="Show detailed logs")

    args = parser.parse_args()
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(project_root, "config", "class_content_validation.json")
    validator = ClassContentValidator(args.class_num, args.content_dir, config_path, args.verbose)
    validator.validate_chapter_packages()
    validator.validate_master_data()
    validator.validate_multimedia()
    validator.check_contamination()
    validator.check_production_safety()
    validator.generate_report()
    print(f"\nValidation complete. Report saved to {args.content_dir}")

if __name__ == "__main__":
    main()
