import os
import re

frontend_dir = r"D:\GURUKUL\frontend-nextjs\src"

print("==========================================================================")
print("AUDITING FRONTEND FOR UNGUARDED .replace() CALLS")
print("==========================================================================\n")

for root, dirs, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith(".tsx") or f.endswith(".ts"):
            fpath = os.path.join(root, f)
            content = open(fpath, encoding="utf-8").read()
            for line_idx, line in enumerate(content.splitlines(), 1):
                if ".replace(" in line:
                    print(f"File: {os.path.relpath(fpath, frontend_dir)} : Line {line_idx}")
                    print(f"  {line.strip()}")
                    print("-" * 60)

if __name__ == "__main__":
    pass
