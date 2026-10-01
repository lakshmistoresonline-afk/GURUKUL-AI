import json

path = r"D:/GURUKUL/ProcessedContent/Class7/Hindi/G7-HIN-U01-C01/question_papers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Papers count:", len(data.get("question_papers", [])))
for p in data.get("question_papers", []):
    print("Paper title:", p.get("paper_title"))
    for s in p.get("sections", []):
        print("  Section title/name:", s.get("section_title") or s.get("section_name"))
        print("  Questions count:", len(s.get("questions", [])))
        for q in s.get("questions", [])[:5]:
            print("    -", q.get("question_text") or q.get("q"))
