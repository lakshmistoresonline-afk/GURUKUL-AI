from pathlib import Path

p = Path(r"D:\GURUKUL-AI\generate_ground_truth_certification.py")

s = p.read_text(encoding="utf-8-sig")

old = '''    roots = [
        repo_root / "generation_staging",
        repo_root / "backend",
        repo_root / "runtime-data",
        repo_root / "Contents",
    ]'''

new = '''    roots = [
        repo_root,
        repo_root / "generation_staging",
        repo_root / "backend",
        repo_root / "runtime-data",
        repo_root / "Contents",
    ]'''

if old not in s:
    raise SystemExit("PATCH FAILED: expected roots block was not found.")

s = s.replace(old, new, 1)

p.write_text(s, encoding="utf-8")

print("CERTIFICATION EVIDENCE ROOT PATCH COMPLETE")
