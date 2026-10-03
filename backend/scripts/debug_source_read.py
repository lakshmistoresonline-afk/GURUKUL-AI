import os
import json

AUTH_SOURCE_ROOT = r"D:/GURUKUL/Contents/Question Bank"

for root, dirs, files in os.walk(AUTH_SOURCE_ROOT):
    for file in files:
        if file == "paper_questions_unique.json":
            sp = os.path.join(root, file)
            try:
                with open(sp, "r", encoding="utf-8") as sf:
                    sdata = json.load(sf)
                    for q in sdata.get("questions", []):
                        pass
            except Exception as e:
                print(f"Failed on {sp}: {e}")
