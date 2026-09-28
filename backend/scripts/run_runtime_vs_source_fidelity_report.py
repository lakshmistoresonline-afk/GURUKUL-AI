import os
import json
import urllib.request
import urllib.parse

print("==========================================================================")
print("RUNTIME DASHBOARD VS SOURCE DATA FIDELITY REPORT")
print("==========================================================================\n")

BASE_URL = "http://localhost:8080/api/v1"

def fetch_json(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return None

classes_data = fetch_json(f"{BASE_URL}/classes")
if not classes_data:
    print("Error: FastAPI backend is not running at http://localhost:8080")
    exit(1)

total_checked = 0
fidelity_comparisons = []

for cls_obj in classes_data:
    grade = cls_obj.get("grade")
    subjects = cls_obj.get("subjects", [])
    for subj in subjects:
        encoded_subj = urllib.parse.quote(subj)
        subj_data = fetch_json(f"{BASE_URL}/classes/{grade}/subjects/{encoded_subj}")
        if not subj_data:
            continue

        for unit in subj_data.get("units", []):
            for ch in unit.get("chapters", []):
                ch_id = ch.get("id")
                source_data = fetch_json(f"{BASE_URL}/chapters/{ch_id}/source?grade={grade}&subject={encoded_subj}")
                if not source_data or "sections" not in source_data:
                    continue

                sections = source_data.get("sections", {})
                ov = sections.get("overview", {}) or {}

                # Extract overview summary length from runtime API
                runtime_summary = ""
                if isinstance(ov, dict):
                    runtime_summary = ov.get("summary") or ov.get("overview") or ov.get("core_summary") or ov.get("description") or ""

                # Load corresponding source overview summary directly from disk
                # Subject folder mapping
                subj_folder_map = {
                    "English": "English",
                    "Hindi": "Hindi",
                    "Maths": "Maths",
                    "Science": "Science",
                    "Social": "Social",
                    "Maths I": "Maths I",
                    "Maths II": "Maths II",
                    "Social I": "Social I",
                    "Social II": "Social II"
                }
                folder_name = subj_folder_map.get(subj, subj)
                source_path = os.path.join(r"D:\GURUKUL\Contents", f"Class {grade}", folder_name, "Overview.json")

                source_summary = ""
                if os.path.exists(source_path):
                    try:
                        with open(source_path, "r", encoding="utf-8") as sf:
                            s_json = json.load(sf)
                            s_chapters = s_json.get("chapters", [])
                            # Match chapter
                            for s_idx, s_ch in enumerate(s_chapters):
                                s_num = s_ch.get("chapter_number") or s_ch.get("chapterNumber") or (s_idx + 1)
                                if s_num == ch.get("chapterNumber") or f"C{s_num:02d}" in ch_id:
                                    source_summary = s_ch.get("summary") or s_ch.get("overview") or s_ch.get("core_summary") or s_ch.get("description") or ""
                                    break
                    except Exception:
                        pass

                total_checked += 1
                runtime_chars = len(str(runtime_summary))
                source_chars = len(str(source_summary))

                fidelity_comparisons.append({
                    "grade": grade,
                    "subject": subj,
                    "chapterId": ch_id,
                    "chapterTitle": ch.get("title"),
                    "sourceChars": source_chars,
                    "runtimeChars": runtime_chars,
                    "match": source_chars == runtime_chars
                })

print(f"Total Chapters Character-Fidelity Checked at Runtime: {total_checked}")
mismatches = [f for f in fidelity_comparisons if not f["match"]]
print(f"Character Length Mismatches Found: {len(mismatches)}")

report_output = {
    "totalChecked": total_checked,
    "mismatchesCount": len(mismatches),
    "comparisons": fidelity_comparisons
}

report_path = r"D:\GURUKUL\reports\RUNTIME_VS_SOURCE_FIDELITY_REPORT.json"
os.makedirs(os.path.dirname(report_path), exist_ok=True)
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report_output, f, ensure_ascii=False, indent=2)

print(f"\nRuntime vs Source Fidelity Report Saved to {report_path}")
