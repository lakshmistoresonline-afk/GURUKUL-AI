from pathlib import Path
import re
import sys

EVIDENCE = Path("CANONICAL_VALIDATION_PROMOTION_EVIDENCE.txt")

print("CANONICAL EVIDENCE DIRECT VALIDATION")
print("-------------------------------------")
print(f"File exists       : {EVIDENCE.exists()}")

if not EVIDENCE.exists():
    print("CANONICAL PASS    : False")
    sys.exit(1)

raw = EVIDENCE.read_bytes()
print(f"File size         : {len(raw)}")

# Evidence is UTF-16 LE with BOM.
try:
    text = raw.decode("utf-16")
except UnicodeDecodeError:
    try:
        text = raw.decode("utf-16-le")
    except UnicodeDecodeError:
        print("ERROR             : Unable to decode canonical evidence")
        print("CANONICAL PASS    : False")
        sys.exit(1)

def check(pattern):
    return bool(re.search(pattern, text, re.IGNORECASE))

checks = {
    "jobs_136":           check(r"Jobs\s*:\s*136"),
    "validated_136":      check(r"Validated\s*:\s*136"),
    "failed_0":           check(r"Failed\s*:\s*0"),
    "promotable_136":     check(r"Promotable\s*:\s*136"),
    "promoted_440":       check(r"Promoted files\s*:\s*440"),
    "promotion_complete": check(r"PROMOTION COMPLETE"),
}

for name, value in checks.items():
    print(f"{name:<20}: {value}")

passed = all(checks.values())

print("-------------------------------------")
print(f"CANONICAL PASS    : {passed}")

if not passed:
    sys.exit(1)

sys.exit(0)
