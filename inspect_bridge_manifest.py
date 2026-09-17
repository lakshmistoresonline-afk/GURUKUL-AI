import json
from pathlib import Path

p = Path("generation_staging/20260909T083940Z/V4_CANONICAL_BRIDGE_MANIFEST.json")
d = json.loads(p.read_text(encoding="utf-8-sig"))

print("=" * 100)
print("BRIDGE MANIFEST STRUCTURE")
print("=" * 100)

print("Top-level keys:")
for k, v in d.items():
    if isinstance(v, dict):
        print(f"  {k}: dict ({len(v)} entries)")
    elif isinstance(v, list):
        print(f"  {k}: list ({len(v)} entries)")
    else:
        print(f"  {k}: {type(v).__name__} = {v}")

print()
print("=" * 100)
print("ALL FAILURE/ERROR INFORMATION")
print("=" * 100)

def walk(obj, path="ROOT"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = str(k).lower()
            if any(x in key for x in ["fail", "error", "reason", "status"]):
                if not isinstance(v, (dict, list)):
                    print(f"{path}.{k} = {v}")
            walk(v, f"{path}.{k}")

    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, f"{path}[{i}]")

walk(d)

print()
print("=" * 100)
print("MANIFEST JSON")
print("=" * 100)
print(json.dumps(d, ensure_ascii=False, indent=2))
