import json
import os

path = r"D:/GURUKUL/reports/QUESTION_BANK_VERIFICATION_REPORT.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

errors = data.get("errors", [])
print(f"Total errors: {len(errors)}")
for err in errors[:20]:
    print(" -", err)
