import json
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, "General Learning", "Gurukul_General_Learning_Classes_5_6_7_Max_V1.json")

def validate():
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data file not found at {DATA_PATH}")
        return

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    content = data.get('content', [])
    report = {
        "total_records": len(content),
        "by_class": {},
        "by_type": {},
        "errors": []
    }

    seen_ids = set()

    for idx, item in enumerate(content):
        # 1. Common Fields
        item_id = item.get('id')
        item_type = item.get('type')
        class_id = item.get('classId')

        if not item_id:
            report["errors"].append(f"Record {idx}: Missing ID")
        elif item_id in seen_ids:
            report["errors"].append(f"Record {idx}: Duplicate ID {item_id}")
        seen_ids.add(item_id)

        if not item_type:
            report["errors"].append(f"Record {idx} ({item_id}): Missing type")

        if class_id is None:
            report["errors"].append(f"Record {idx} ({item_id}): Missing classId")

        # Stats
        class_key = f"class_{class_id}" if class_id else "unknown"
        report["by_class"][class_key] = report["by_class"].get(class_key, 0) + 1
        report["by_type"][item_type] = report["by_type"].get(item_type, 0) + 1

        # 2. Type-specific validation
        if item_type == "vocabulary":
            required = ['word', 'meaning', 'example', 'practice']
            for field in required:
                if not item.get(field):
                    report["errors"].append(f"{item_id}: Missing field {field}")

            practice = item.get('practice', {})
            if not practice.get('question') or not practice.get('answer'):
                report["errors"].append(f"{item_id}: Incomplete practice data")

        elif item_type in ["general_knowledge", "brain_boost"]:
            required = ['topic', 'question', 'options', 'answer']
            for field in required:
                if not item.get(field):
                    report["errors"].append(f"{item_id}: Missing field {field}")

            options = item.get('options', [])
            answer = item.get('answer')
            if options and answer not in options:
                report["errors"].append(f"{item_id}: Answer '{answer}' not in options")

    # Final Summary
    print("--- General Learning Data Validation Report ---")
    print(f"Total Records: {report['total_records']}")
    print("\nBy Class:")
    for k, v in report['by_class'].items():
        print(f"  {k}: {v}")

    print("\nBy Type:")
    for k, v in report['by_type'].items():
        print(f"  {k}: {v}")

    if report["errors"]:
        print(f"\nErrors Found: {len(report['errors'])}")
        for err in report["errors"][:20]: # Show first 20
            print(f"  - {err}")
        if len(report["errors"]) > 20:
            print(f"  ... and {len(report['errors']) - 20} more errors.")
    else:
        print("\nValidation Status: PASSED ✅")

    # Save report to artifacts for the AI
    report_file = os.path.join(os.path.dirname(__file__), "general_learning_validation_report.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    validate()
