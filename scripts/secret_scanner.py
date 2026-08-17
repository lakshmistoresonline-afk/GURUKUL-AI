import os
import re
import subprocess
import sys

# Detection Patterns
PATTERNS = {
    "Private Key": r"-----BEGIN[ \t]+(?:RSA[ \t]+|OPENSSH[ \t]+|EC[ \t]+|DSA[ \t]+)?PRIVATE[ \t]+KEY-----",
    "AWS Access Key": r"(?:^|[^A-Za-z0-9_])AKIA[0-9A-Z]{16}(?:[^A-Za-z0-9_]|$)",
    "GitHub Token": r"(?:^|[^A-Za-z0-9_])gh[pousr]_[A-Za-z0-9_]{30,}(?:[^A-Za-z0-9_]|$)",
    "Generic Bearer": r"[Bb][Ee][Aa][Rr][Ee][Rr][ \t]+[A-Za-z0-9._-]{30,}",
    # Only match literal strings, not variable lookups like settings.KEY
    "Secret Assignment": r"(?:api[_-]?key|secret[_-]?key|access[_-]?token|private[_-]?key)[ \t]*[:=][ \t]*[\"'][A-Za-z0-9_./+:=:-]{20,}[\"']",
    "sk-Key": r"sk-(?:proj-|admin-|svcacct-)?[A-Za-z0-9_-]{20,}"
}

# Directories to ignore
EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".next", "out", "storage"}
# Files to ignore
EXCLUDE_FILES = {"secret_scanner.py", "package-lock.json", "yarn.lock", "pnpm-lock.yaml"}

def scan():
    print("--- Gurukul AI Secret Scanner ---")
    findings = []

    # 1. Get staged files from Git
    try:
        staged_files = subprocess.check_output(["git", "diff", "--cached", "--name-only"], text=True).splitlines()
    except subprocess.CalledProcessError:
        print("Error: Not a git repository or Git not found.")
        return False

    if not staged_files:
        print("No staged files found to scan.")
        return True

    for file_path in staged_files:
        if not os.path.isfile(file_path): continue
        if any(d in file_path.split(os.sep) for d in EXCLUDE_DIRS): continue
        if os.path.basename(file_path) in EXCLUDE_FILES: continue

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_num, line in enumerate(f, 1):
                    for name, pattern in PATTERNS.items():
                        # Crucial: Don't match the pattern definition itself
                        if name == "Private Key" and "PATTERNS =" in line: continue

                        match = re.search(pattern, line)
                        if match:
                            # Verify it's not a literal regex or pattern definition
                            if "r\"" in line or 'r\'' in line: continue

                            findings.append(f"{file_path}:{line_num} - Possible {name} detected")
        except Exception as e:
            print(f"Warning: Could not scan {file_path}: {e}")

    if findings:
        print("\n!!! SENSITIVE DATA DETECTED !!!")
        for f in findings[:20]:
            print(f)
        if len(findings) > 20:
            print(f"... and {len(findings) - 20} more.")
        return False

    print("Scan complete. No likely secrets found in staged files.")
    return True

if __name__ == "__main__":
    if not scan():
        sys.exit(1)
    sys.exit(0)
