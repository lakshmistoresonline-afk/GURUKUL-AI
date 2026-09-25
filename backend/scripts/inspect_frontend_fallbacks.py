import os

page_path = r"D:\GURUKUL\frontend-nextjs\src\app\page.tsx"
client_path = r"D:\GURUKUL\frontend-nextjs\src\app\[grade]\[subject]\[chapterId]\ChapterClient.tsx"

print("Checking page.tsx for fallbacks:")
if os.path.exists(page_path):
    txt = open(page_path, encoding="utf-8").read()
    print("  Contains FALLBACK_CLASS5_ENGLISH:", "FALLBACK_CLASS5_ENGLISH" in txt)
    print("  Contains fetch /api/v1:", "/api/v1" in txt)

print("\nChecking ChapterClient.tsx for fallbacks:")
if os.path.exists(client_path):
    txt2 = open(client_path, encoding="utf-8").read()
    print("  Contains fallback blocks:", "fallback" in txt2.lower() or "mock" in txt2.lower())
    print("  Contains fetch /api/v1:", "/api/v1" in txt2)
