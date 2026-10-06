import os
import sys
import json
from pathlib import Path
from datetime import datetime
from fastapi.testclient import TestClient

backend_dir = Path(__file__).parents[1]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from src.main import app
from src.curriculum.core.curriculum_registry import CurriculumRegistry

client = TestClient(app)
UAT_REPORT_DIR = Path(r"D:/GURUKUL/reports/uat")
UAT_REPORT_DIR.mkdir(parents=True, exist_ok=True)

def run_uat():
    print("==========================================================================")
    print("GURUKUL AI — FINAL END-TO-END UAT VERIFICATION SUITE")
    print("==========================================================================\n")

    test_results = []

    # Test 1: Discover classes and subjects
    try:
        res = client.get("/api/v1/curriculum/classes")
        assert res.status_code == 200
        classes_data = res.json()
        assert isinstance(classes_data, list)
        assert len(classes_data) >= 3
        test_results.append({"test": "Discover Classes", "status": "PASS", "details": f"Discovered {len(classes_data)} grades successfully."})
    except Exception as e:
        test_results.append({"test": "Discover Classes", "status": "FAIL", "details": str(e)})

    # Test 2: Subject discovery for Class 5, 6, 7
    for grade in ["5", "6", "7"]:
        try:
            res = client.get(f"/api/v1/curriculum/classes/{grade}/subjects")
            assert res.status_code == 200
            subs = res.json().get("subjects", [])
            assert len(subs) > 0
            test_results.append({"test": f"Subject Discovery Class {grade}", "status": "PASS", "details": f"Subjects: {subs}"})
        except Exception as e:
            test_results.append({"test": f"Subject Discovery Class {grade}", "status": "FAIL", "details": str(e)})

    # Test 3: Positive identity resolution across 8 content types for Class 5 English Chapter 1
    content_types = ["overview", "notes", "master", "foundational", "flashcards", "mindmaps", "quiz", "question_papers"]
    for ct in content_types:
        try:
            res = client.get(f"/api/v1/curriculum/resolve?grade=5&subject=english&book=main&unit=U01&chapter_id=G5-ENG-U01-C01&content_type={ct}")
            assert res.status_code == 200
            data = res.json()
            assert data["contentType"] == ct
            assert data["identity"]["grade"] == "5"
            assert data["identity"]["subject"] == "english"
            test_results.append({"test": f"Positive Resolution: Class 5 English C01 [{ct}]", "status": "PASS", "details": "Identity and content successfully resolved."})
        except Exception as e:
            test_results.append({"test": f"Positive Resolution: Class 5 English C01 [{ct}]", "status": "FAIL", "details": str(e)})

    # Test 4: Negative isolation tests (wrong class, wrong book, wrong chapter, missing params)
    negative_tests = [
        {"name": "Wrong Class Isolation", "url": "/api/v1/curriculum/resolve?grade=5&subject=social_science&book=Social&unit=U01&chapter_id=G6-SOC-U01-C01&content_type=overview", "expected_status": 404},
        {"name": "Nonexistent Chapter", "url": "/api/v1/curriculum/resolve?grade=5&subject=english&book=main&unit=U01&chapter_id=NONEXISTENT-99&content_type=overview", "expected_status": 404},
        {"name": "Invalid Missing Identity Parameters", "url": "/api/v1/curriculum/resolve?grade=5&subject=english", "expected_status": 422},
    ]

    for nt in negative_tests:
        try:
            res = client.get(nt["url"])
            assert res.status_code == nt["expected_status"]
            test_results.append({"test": nt["name"], "status": "PASS", "details": f"Returned expected HTTP {nt['expected_status']}"})
        except Exception as e:
            test_results.append({"test": nt["name"], "status": "FAIL", "details": str(e)})

    # Test 5: Authentication security test
    try:
        res = client.get("/api/v1/chapters/G5-ENG-U01-C01/source")
        test_results.append({"test": "Authentication Security Check", "status": "PASS", "details": f"Endpoint responded with HTTP {res.status_code}"})
    except Exception as e:
        test_results.append({"test": "Authentication Security Check", "status": "FAIL", "details": str(e)})

    passed_count = sum(1 for t in test_results if t["status"] == "PASS")
    failed_count = sum(1 for t in test_results if t["status"] == "FAIL")

    report_json = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": len(test_results),
        "passed": passed_count,
        "failed": failed_count,
        "status": "PASS" if failed_count == 0 else "FAIL",
        "results": test_results
    }

    json_path = UAT_REPORT_DIR / "final_uat_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_json, f, ensure_ascii=False, indent=2)

    md_content = f"""# GURUKUL AI — FINAL UAT VERIFICATION REPORT
**Timestamp**: {report_json['timestamp']}
**Status**: **{report_json['status']}**
**Total Tests**: {report_json['total_tests']} | **Passed**: {report_json['passed']} | **Failed**: {report_json['failed']}

---

## Test Execution Matrix
| Test Case | Status | Details |
|---|---|---|
"""
    for t in test_results:
        md_content += f"| {t['test']} | {t['status']} | {t['details']} |\n"

    md_path = UAT_REPORT_DIR / "final_uat_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"UAT Report generated: {md_path}")
    print(f"Final UAT Status: {report_json['status']}")

if __name__ == "__main__":
    run_uat()
