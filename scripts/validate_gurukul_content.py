import os
import json
import logging
import re
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = "D:/GURUKUL-AI"
MASTER_CONTENT_ROOT = os.path.join(PROJECT_ROOT, "backend", "GURUKUL_AI_FINAL_MASTER_CONTENT_CLASSES_5_6_7")

def validate_content():
    report = {
        "classes": {},
        "total_chapters": 0,
        "errors": [],
        "warnings": []
    }

    for c in [5, 6, 7]:
        class_key = f"class_{c}"
        class_dir = os.path.join(MASTER_CONTENT_ROOT, f"Class {c}")
        index_path = os.path.join(class_dir, f"Class_{c}_Master_Index.json")

        if not os.path.exists(index_path):
            report["errors"].append(f"Master Index missing for Class {c}")
            continue

        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)

        chapters = index.get("chapters", [])
        report["classes"][class_key] = {
            "chapter_count": len(chapters),
            "subjects": index.get("subjects", []),
            "validations": []
        }
        report["total_chapters"] += len(chapters)

        for chap in chapters:
            pkg_rel_path = chap["path"]
            pkg_abs_path = os.path.join(class_dir, "..", pkg_rel_path)

            chap_id = chap["chapterId"]
            chap_res = {"id": chap_id, "status": "PASS", "issues": []}

            if not os.path.exists(pkg_abs_path):
                chap_res["status"] = "FAIL"
                chap_res["issues"].append("package.json missing")
                report["errors"].append(f"Missing file: {pkg_abs_path}")
            else:
                try:
                    with open(pkg_abs_path, 'r', encoding='utf-8') as f:
                        pkg = json.load(f)

                    # 1. Metadata check
                    metadata = pkg.get("metadata", {})
                    if not metadata:
                        chap_res["issues"].append("Missing metadata")
                    elif metadata.get("chapterId") != chap_id:
                        chap_res["issues"].append(f"Chapter ID mismatch: index={chap_id}, package={metadata.get('chapterId')}")

                    # 2. Content check
                    content = pkg.get("content", {})
                    if not content:
                        chap_res["issues"].append("Missing content")
                    else:
                        if not content.get("introduction") and not content.get("detailedLesson", {}).get("overview"):
                             chap_res["issues"].append("Empty introduction")
                        if not content.get("teacher_explanation") and not content.get("teacherExplanation") and not content.get("detailedLesson", {}).get("overview"):
                             chap_res["issues"].append("Missing teacher explanation")

                    # 3. Concepts/Mastery check
                    concepts = pkg.get("original_data", {}).get("aiEnrichment", {}).get("concepts", [])
                    if not concepts:
                         concepts = pkg.get("original_data", {}).get("mastery", {}).get("mappings", [])

                    if not concepts:
                        chap_res["issues"].append("No concepts or mappings found")
                    else:
                        for idx, con in enumerate(concepts):
                            if not con.get("conceptId") and not con.get("id"):
                                chap_res["issues"].append(f"Concept at index {idx} missing ID")
                            if not con.get("name") and not con.get("conceptName") and not con.get("concept"):
                                chap_res["issues"].append(f"Concept {con.get('conceptId') or idx} missing Name")

                    # 4. Assessment check
                    assessment = pkg.get("original_data", {}).get("assessment", {})
                    bank = assessment.get("expandedQuestionBank", [])
                    if not bank:
                         bank = pkg.get("original_data", {}).get("aiEnrichment", {}).get("question_bank", [])

                    if not bank:
                        chap_res["issues"].append("Empty question bank")
                    elif len(bank) < 5:
                        chap_res["issues"].append(f"Thin question bank: only {len(bank)} items")

                    if chap_res["issues"]:
                        chap_res["status"] = "WARNING" if all("thin" in i.lower() or "missing" in i.lower() for i in chap_res["issues"]) else "FAIL"
                        if chap_res["status"] == "FAIL":
                             report["errors"].append(f"Validation failed for {chap_id}: {', '.join(chap_res['issues'])}")
                        else:
                             report["warnings"].append(f"Warning for {chap_id}: {', '.join(chap_res['issues'])}")

                except Exception as e:
                    chap_res["status"] = "FAIL"
                    chap_res["issues"].append(f"JSON Parse Error: {e}")
                    report["errors"].append(f"JSON Error in {chap_id}: {e}")

            report["classes"][class_key]["validations"].append(chap_res)

    # Save final report
    report_path_json = os.path.join(PROJECT_ROOT, "GURUKUL_CONTENT_VALIDATION_REPORT.json")
    report_path_md = os.path.join(PROJECT_ROOT, "GURUKUL_CONTENT_VALIDATION_REPORT.md")

    with open(report_path_json, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    with open(report_path_md, 'w', encoding='utf-8') as f:
        f.write("# Gurukul Content Validation Report\n\n")
        f.write(f"Total Chapters: {report['total_chapters']}\n")
        f.write(f"Errors: {len(report['errors'])}\n")
        f.write(f"Warnings: {len(report['warnings'])}\n\n")

        if report["errors"]:
            f.write("## Critical Errors\n")
            for err in report["errors"][:50]: # Cap to 50
                f.write(f"* {err}\n")
            if len(report["errors"]) > 50: f.write("* ... and more\n")

    print(f"Validation complete. Errors: {len(report['errors'])}, Warnings: {len(report['warnings'])}")

if __name__ == "__main__":
    validate_content()
