import json
from pathlib import Path

p = Path("generation_staging/20260909T083940Z/V4_CANONICAL_BRIDGE_MANIFEST.json")

d = json.loads(p.read_text(encoding="utf-8-sig"))

print("=" * 100)
print("FAILED CANONICAL JOBS")
print("=" * 100)

entries = d.get("jobs") or d.get("entries") or d.get("manifest") or []

if isinstance(entries, dict):
    entries = list(entries.values())

failed = []

for x in entries:
    if not isinstance(x, dict):
        continue

    status = str(x.get("status", "")).lower()

    if status not in ("validated", "promoted", "pass", "passed"):
        failed.append(x)

print("Failures:", len(failed))
print()

for i, x in enumerate(failed, 1):
    print(f"--- FAILURE {i} ---")
    print(json.dumps(x, ensure_ascii=False, indent=2))
    print()

print("=" * 100)
