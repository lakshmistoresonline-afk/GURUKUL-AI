import json
from pathlib import Path

p = Path("generation_staging/20260909T083940Z/V4_CANONICAL_BRIDGE_MANIFEST.json")
d = json.loads(p.read_text(encoding="utf-8-sig"))

print("=" * 100)
print("EXACT CANONICAL FAILURES")
print("=" * 100)

failed = [
    x for x in d["chapters"]
    if x.get("status") != "validated"
]

print("Failures:", len(failed))
print()

for n, x in enumerate(failed, 1):
    print(f"--- FAILURE {n} ---")
    print(json.dumps(x, ensure_ascii=False, indent=2))
    print()

print("=" * 100)
