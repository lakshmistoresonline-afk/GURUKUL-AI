import argparse
import json
import subprocess
import sys
import os
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    validator = root / "backend" / "scripts" / "generate_all_valid_contents.py"

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    p = subprocess.run(
        [sys.executable, str(validator), "--repo-root", str(root)],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )

    output = (p.stdout or "") + "\n" + (p.stderr or "")

    marker = "=== GURUKUL REPOSITORY-WIDE SUMMARY ==="

    if marker not in output:
        print("ERROR: Official summary marker not found.")
        print(output[-10000:])
        raise SystemExit(2)

    after = output.split(marker, 1)[1]

    start = after.find("{")
    end = after.find("}", start)

    # Find the complete JSON object safely.
    depth = 0
    in_string = False
    escape = False
    json_end = None

    for i in range(start, len(after)):
        c = after[i]

        if in_string:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == '"':
                in_string = False
            continue

        if c == '"':
            in_string = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                json_end = i + 1
                break

    if json_end is None:
        print("ERROR: Could not isolate official JSON summary.")
        raise SystemExit(3)

    summary = json.loads(after[start:json_end])

    print()
    print("=" * 80)
    print("GURUKUL AI — FINAL REPOSITORY INVENTORY")
    print("=" * 80)

    for key in [
        "classes",
        "subject_packages",
        "chapters",
        "missing_pillar_instances",
        "placeholder_files_detected",
        "invalid_json_files_detected",
    ]:
        print(f"{key:32}: {summary.get(key)}")

    status = summary.get("status_counts", {})

    print(f"{'complete':32}: {status.get('complete', 0)}")
    print(f"{'planned':32}: {status.get('planned', 0)}")

    print("=" * 80)

    report = {
        "summary": summary,
        "validator_exit_code": p.returncode,
    }

    report_file = root / "pending_chapters_final_report.json"
    report_file.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Report: {report_file}")

    if p.returncode != 0:
        print()
        print("NOTE: Validator returned a non-zero code because gaps remain.")
        print("The inventory itself was successfully extracted.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())