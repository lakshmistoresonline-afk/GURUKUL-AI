import os
import json
import urllib.request
import urllib.parse
import urllib.error

print("==========================================================================")
print("RUNTIME API VERIFICATION AUDIT (ALL CLASSES, SUBJECTS, CHAPTERS)")
print("==========================================================================\n")

BASE_URL = "http://localhost:8080/api/v1"

def test_endpoint(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            return True, data
    except Exception as e:
        return False, str(e)

classes_ok, classes_data = test_endpoint(f"{BASE_URL}/classes")
print(f"1. Classes Discovery Endpoint (/classes): {'SUCCESS' if classes_ok else 'FAILED'}")

audit_results = {
    "timestamp": "2025-03-30T12:00:00Z",
    "classesEndpointStatus": "SUCCESS" if classes_ok else "FAILED",
    "classesDiscovered": classes_data if classes_ok else [],
    "subjectsTested": 0,
    "chaptersTested": 0,
    "apiFailures": []
}

if classes_ok and isinstance(classes_data, list):
    for cls_obj in classes_data:
        grade = cls_obj.get("grade")
        subjects = cls_obj.get("subjects", [])
        for subj in subjects:
            audit_results["subjectsTested"] += 1
            encoded_subj = urllib.parse.quote(subj)
            subj_url = f"{BASE_URL}/classes/{grade}/subjects/{encoded_subj}"
            subj_ok, subj_data = test_endpoint(subj_url)
            if not subj_ok:
                audit_results["apiFailures"].append({
                    "type": "SUBJECT_ENDPOINT_FAIL",
                    "grade": grade,
                    "subject": subj,
                    "error": subj_data
                })
                continue

            units = subj_data.get("units", [])
            for unit in units:
                chapters = unit.get("chapters", [])
                for ch in chapters:
                    audit_results["chaptersTested"] += 1
                    ch_id = ch.get("id")
                    ch_url = f"{BASE_URL}/chapters/{ch_id}/source?grade={grade}&subject={encoded_subj}"
                    ch_ok, ch_data = test_endpoint(ch_url)
                    if not ch_ok:
                        audit_results["apiFailures"].append({
                            "type": "CHAPTER_SOURCE_FAIL",
                            "grade": grade,
                            "subject": subj,
                            "chapterId": ch_id,
                            "error": ch_data
                        })
                    else:
                        sections = ch_data.get("sections", {})
                        for sec_name, sec_val in sections.items():
                            if sec_val is None and sec_name not in ["flashcards", "quiz"]:
                                audit_results["apiFailures"].append({
                                    "type": "SECTION_NULL_FAIL",
                                    "grade": grade,
                                    "subject": subj,
                                    "chapterId": ch_id,
                                    "section": sec_name
                                })

print(f"\nTotal Subjects Tested: {audit_results['subjectsTested']}")
print(f"Total Chapters Tested: {audit_results['chaptersTested']}")
print(f"Total API Failures Found: {len(audit_results['apiFailures'])}")

report_path = r"D:\GURUKUL\reports\RUNTIME_API_VERIFICATION_REPORT.json"
os.makedirs(os.path.dirname(report_path), exist_ok=True)
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(audit_results, f, ensure_ascii=False, indent=2)

print(f"\nFull Runtime API Verification Report Saved to {report_path}")
