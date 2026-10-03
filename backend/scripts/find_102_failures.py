import os
import sys
import json
import traceback

AUTH_SOURCE_ROOT = r"D:/GURUKUL/Contents/Question Bank"

failures = 0
for root, dirs, files in os.walk(AUTH_SOURCE_ROOT):
    for file in files:
        if file == "paper_questions_unique.json":
            sp = os.path.join(root, file)
            try:
                with open(sp, "r", encoding="utf-8") as sf:
                    sdata = json.load(sf)
                    for idx, q in enumerate(sdata.get("questions", [])):
                        try:
                            qid = q.get("question_id")
                            pid = q.get("paper_id")
                            q_obj = q.get("question") if isinstance(q.get("question"), dict) else q
                            # Test if q_obj is a dict or string or something else
                            if not isinstance(q_obj, (dict, str, int, float)):
                                raise TypeError(f"Unexpected type: {type(q_obj)}")
                        except Exception as e:
                            failures += 1
                            print(f"Failed in {sp} at idx {idx}: {e}")
            except Exception as e:
                pass

print("Total failures found:", failures)
