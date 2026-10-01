import json

ledger_path = r"D:/GURUKUL/reports/THREE_WAY_QUESTION_FORENSIC_LEDGER.json"
with open(ledger_path, "r", encoding="utf-8") as f:
    ledger = json.load(f)

print("Papa's Spectacles Trace (QP-0116 to QP-0127):")
for item in ledger:
    if "01_Papa_s_Spectacles" in item["source_path"] and item["source_question_id"] in [f"QP-{i:04d}" for i in range(116, 128)]:
        print(f" - {item['source_question_id']}: Github Present={item['github_baseline_present']}, Current Present={item['current_present']}, Classification={item['classification']}")
