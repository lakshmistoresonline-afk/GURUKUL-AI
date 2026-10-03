import os
import json

AUTH_SOURCE_ROOT = r"D:/GURUKUL/Contents/Question Bank"

errs = 0
for root, dirs, files in os.walk(AUTH_SOURCE_ROOT):
    for file in files:
        if file == "paper_questions_unique.json":
            sp = os.path.join(root, file)
            try:
                with open(sp, "r", encoding="utf-8") as sf:
                    json.load(sf)
            except Exception as e:
                errs += 1
                print(f"Error: {sp} -> {e}")

print("Total parse errors:", errs)
