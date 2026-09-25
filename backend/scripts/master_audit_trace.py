import sys
import os
import json
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def execute_master_audit():
    p = r"D:\GURUKUL\Contents\Class 5\English"
    files = sorted(os.listdir(p))

    print("==========================================================================")
    print("MASTER AUDIT: SOURCE-TO-FRONTEND TRACE FOR ALL 10 DATASETS")
    print("==========================================================================\n")

    audit_results = {}

    for fname in files:
        fpath = os.path.join(p, fname)
        size = os.path.getsize(fpath)
        raw_bytes = open(fpath, "rb").read()
        sha = hashlib.sha256(raw_bytes).hexdigest()
        data = json.loads(raw_bytes.decode("utf-8"))

        # Determine dataset structure
        root_type = type(data).__name__
        top_keys = list(data.keys()) if isinstance(data, dict) else []

        # Check chapter & record counts
        records_count = 0
        if "chapters" in data and isinstance(data["chapters"], list):
            records_count = len(data["chapters"])
        elif "cards" in data and isinstance(data["cards"], list):
            records_count = len(data["cards"])
        elif "questions" in data and isinstance(data["questions"], list):
            records_count = len(data["questions"])
        elif "units" in data and isinstance(data["units"], list):
            records_count = len(data["units"])

        audit_results[fname] = {
            "size": size,
            "sha256": sha,
            "root_type": root_type,
            "top_keys": top_keys,
            "records_count": records_count,
            "data": data
        }

        print(f"Dataset File: {fname}")
        print(f"  Size: {size} bytes | SHA256: {sha}")
        print(f"  Root Type: {root_type} | Top Keys: {top_keys}")
        print(f"  Primary Records Count: {records_count}")
        print("-" * 74)

    return audit_results

if __name__ == "__main__":
    execute_master_audit()
