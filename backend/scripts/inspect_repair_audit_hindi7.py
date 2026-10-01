import json

path = r"D:/GURUKUL/reports/QUESTION_BANK_REPAIR_AUDIT_REPORT.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for res in data.get("audit_results", []):
    if "Class7/Hindi" in res.get("destination_path", ""):
        print(res)
        break
