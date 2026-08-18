import os
import json
from pathlib import Path

ROOT = Path(r"D:\GURUKUL-AI\backend\GURUKUL_AI_CONTENT")

EXPECTED_COMPONENTS = [
    "chapter_metadata", "learning_objectives", "chapter_content",
    "teacher_explanation", "student_explanation", "story_mode",
    "concepts", "assessment_bank", "flashcards", "interactive_lab"
]

def validate():
    issues = []
    total_chapters = 0

    # Load master indexes
    for class_dir in ROOT.glob("class_*"):
        index_path = class_dir / "master_index.json"
        if not index_path.exists():
            issues.append(f"MISSING_INDEX: {class_dir}")
            continue

        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)

        for ch in index.get("chapters", []):
            total_chapters += 1
            chap_path = class_dir / ch["path"].replace("/package.json", "")
            if not chap_path.exists():
                issues.append(f"MISSING_FOLDER: {chap_path}")
                continue

            # Check for required files
            for comp in EXPECTED_COMPONENTS:
                comp_file = chap_path / f"{comp}.json"
                if not comp_file.exists():
                    issues.append(f"MISSING_COMPONENT: {comp} in {ch['chapterId']}")
                else:
                    # Basic JSON validity
                    try:
                        with open(comp_file, 'r', encoding='utf-8') as f:
                            json.load(f)
                    except:
                        issues.append(f"INVALID_JSON: {comp_file}")

    return total_chapters, issues

if __name__ == "__main__":
    count, issues = validate()
    print(f"Validated {count} chapters.")
    if issues:
        print(f"Found {len(issues)} issues.")
        for i in issues[:20]: print(i)
    else:
        print("System integrity verified.")
