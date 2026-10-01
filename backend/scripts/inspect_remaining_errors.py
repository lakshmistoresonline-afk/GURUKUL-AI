import json

path = r"D:/GURUKUL/reports/QUESTION_BANK_VERIFICATION_REPORT.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for err in data.get("errors", []):
    print(" -", err)
