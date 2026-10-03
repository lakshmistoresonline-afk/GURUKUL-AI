import os
import json

verify_dir = r"D:/GURUKUL/reports/production_qb_rebuild_v3_verification_corrected"
# Let's check if there's an error log or check source files directly
from forensic_v9_pure_verifier import AUTH_SOURCE_ROOT, compute_object_fingerprint, get_q_text, normalize_text if 'normalize_text' in globals() else lambda x: x

for root, dirs, files in os.walk(AUTH_SOURCE_ROOT):
    for file in files:
        if file == "paper_questions_unique.json":
            sp = os.path.join(root, file)
            try:
                with open(sp, "r", encoding="utf-8") as sf:
                    json.load(sf)
            except Exception as e:
                print(f"Error parsing {sp}: {e}")
