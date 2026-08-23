import os
import json

PROJECT_ROOT = "D:/GURUKUL-AI"

PATHS_TO_CHECK = [
    os.path.join(PROJECT_ROOT, "JSON FILES", "GURUKUL_CLASSES_5_6_7_ENRICHED_FULL_PACKAGE"),
    os.path.join(PROJECT_ROOT, "JSON FILES", "GURUKUL_CLASSES_5_6_7_TEACHER_EXPLANATION_MASTER"),
    os.path.join(PROJECT_ROOT, "JSON FILES", "GURUKUL_CLASSES_5_6_7_NCERT_CHAPTER_QUESTIONS"),
    os.path.join(PROJECT_ROOT, "Multimedia"),
    os.path.join(PROJECT_ROOT, "Question Bank"),
    os.path.join(PROJECT_ROOT, "General Learning"),
    os.path.join(PROJECT_ROOT, "backend", "storage", "media", "animations"),
    os.path.join(PROJECT_ROOT, "backend", "storage", "media", "videos"),
    os.path.join(PROJECT_ROOT, "backend", "storage", "media", "audio"),
    os.path.join(PROJECT_ROOT, "backend", "storage", "media", "subtitles"),
    os.path.join(PROJECT_ROOT, "backend", "storage", "media", "thumbnails"),
]

FILES_TO_INIT = {
    os.path.join(PROJECT_ROOT, "Multimedia", "GURUKUL_EXTERNAL_MULTIMEDIA_FINAL_163.json"): ({"chapters": []}, "chapters"),
    os.path.join(PROJECT_ROOT, "Multimedia", "GURUKUL_EXTERNAL_MULTIMEDIA_API_IMPORT.json"): ({"resources": []}, "resources"),
    os.path.join(PROJECT_ROOT, "Question Bank", "QUESTION_BANK_MASTER.json"): ({"questions": []}, "questions"),
    os.path.join(PROJECT_ROOT, "General Learning", "Gurukul_General_Learning_Classes_5_6_7_Max_V1.json"): ({"categories": {}}, "categories"),
}

def fix_integrity():
    print("Starting Project Integrity Fix...")

    # 1. Create Directories
    for path in PATHS_TO_CHECK:
        if not os.path.exists(path):
            print(f"Creating missing directory: {path}")
            os.makedirs(path, exist_ok=True)

    # 2. Initialize Critical JSON Files
    for file_path, (default_content, required_key) in FILES_TO_INIT.items():
        needs_init = False
        if not os.path.exists(file_path):
            needs_init = True
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if required_key not in data:
                        print(f"Invalid structure in {file_path}. Resetting...")
                        needs_init = True
            except:
                needs_init = True

        if needs_init:
            print(f"Initializing/Resetting: {file_path}")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(default_content, f, indent=2)

    print("Project Integrity Fix Complete.")

if __name__ == "__main__":
    fix_integrity()
