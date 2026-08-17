import os
import json

PROJECT_ROOT = "D:/GURUKUL-AI"
GL_SOURCE = os.path.join(PROJECT_ROOT, "JSON FINAL", "CLASS 6 FINAL JSONS", "General Learning", "Gurukul_General_Learning_Class_6_Original_V1.json")
GL_TARGET = os.path.join(PROJECT_ROOT, "General Learning", "Gurukul_General_Learning_Classes_5_6_7_Max_V1.json")
MANIFEST_TARGET = os.path.join(PROJECT_ROOT, "frontend-nextjs", "src", "data", "generalLearningManifest.json")

def fix():
    if not os.path.exists(GL_SOURCE):
        print("GL source missing")
        return

    with open(GL_SOURCE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_content = []
    gl_ids = []

    if "categories" in data:
        for cat_name, items in data["categories"].items():
            cat_slug = cat_name.lower().replace(" ", "_").replace("&", "and")
            for i, item in enumerate(items):
                item_id = f"gl_{cat_slug}_{i+1:03d}"
                item["id"] = item_id
                item["category"] = cat_name
                item["type"] = cat_slug
                # Mark as available for all grades to ensure navigation works
                item["availableGrades"] = [5, 6, 7]
                item["classId"] = 6 # Keeping original source grade
                new_content.append(item)
                gl_ids.append(item_id)

    # Save target
    os.makedirs(os.path.dirname(GL_TARGET), exist_ok=True)
    with open(GL_TARGET, 'w', encoding='utf-8') as f:
        json.dump({"content": new_content}, f, indent=2, ensure_ascii=False)

    # Save manifest
    os.makedirs(os.path.dirname(MANIFEST_TARGET), exist_ok=True)
    with open(MANIFEST_TARGET, 'w', encoding='utf-8') as f:
        json.dump(gl_ids, f, indent=2, ensure_ascii=False)

    print(f"Fixed GL integration for all grades. Items: {len(new_content)}")

if __name__ == "__main__":
    fix()
