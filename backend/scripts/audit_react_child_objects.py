import os
import re

renderers_dir = r"D:\GURUKUL\frontend-nextjs\src\renderers"

print("==========================================================================")
print("AUDITING REACT RENDERERS FOR POTENTIAL OBJECTS-AS-REACT-CHILD ERRORS")
print("==========================================================================\n")

for fname in sorted(os.listdir(renderers_dir)):
    if fname.endswith(".tsx"):
        fpath = os.path.join(renderers_dir, fname)
        content = open(fpath, encoding="utf-8").read()
        print(f"File: {fname}")

        # Search for jsx curly brace interpolations
        matches = re.findall(r'\{([^}]+)\}', content)
        for m in matches:
            m_clean = m.strip()
            if any(k in m_clean for k in ["task", "item", "prompt", "val", "data", "element", "v"]):
                if not any(safe in m_clean for safe in ["typeof", "string", "length", "map", "join", "boolean", "idx", "index", "key", "=="]):
                    print(f"  Line candidate: {{{m_clean}}}")
        print("-" * 60)

if __name__ == "__main__":
    pass
